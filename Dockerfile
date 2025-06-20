FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Warsaw

RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3 \
    python3-pip \
    python3-venv \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    build-essential \
    ccache \
    sudo \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

RUN python3 -m pip install --upgrade pip

# Kopiuj requirements.txt do obrazu
COPY requirements.txt .

# Zainstaluj zależności Pythona
RUN python3 -m pip install -r requirements.txt

ENV BUILDOZER_WARN_ON_ROOT=0

WORKDIR /app

# Teraz kopiuj resztę kodu aplikacji
COPY . /app/

RUN mkdir -p /root/.android && echo "count=0" > /root/.android/repositories.cfg

CMD bash -c "\
    echo '🔧 Przygotowywanie środowiska budowania...' && \
    echo '📝 Akceptowanie licencji Android SDK...' && \
    (yes | buildozer android debug) || (echo 'Błąd podczas budowania')"
