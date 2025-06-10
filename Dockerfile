# Dockerfile dla budowania aplikacji Kivy/KivyMD na Androida
FROM ubuntu:20.04

# Ustaw timezone i non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Warsaw

# Zainstaluj podstawowe zależności
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

# Ustaw Java 8 jako domyślną
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Zainstaluj Python dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install \
    buildozer \
    cython==0.29.33 \
    kivy>=2.1.0 \
    kivymd>=1.1.1

# Ustaw Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Wyłącz ostrzeżenie buildozer o root
ENV BUILDOZER_WARN_ON_ROOT=0

# Stwórz użytkownika builduser
RUN useradd -m -s /bin/bash builduser && \
    echo 'builduser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Stwórz katalog roboczy
WORKDIR /app

# Zmień właściciela katalogu
RUN chown -R builduser:builduser /app

# Przełącz na użytkownika builduser
USER builduser

# Kopiuj pliki aplikacji (jako builduser)
COPY --chown=builduser:builduser . /app/

# Domyślna komenda
CMD ["buildozer", "android", "debug"]