# 📱 Budowanie Aplikacji Android z Docker

## 🚀 Szybkie budowanie

### 1. **Zainstaluj Docker**
- Windows/Mac: [Docker Desktop](https://www.docker.com/get-started)
- Linux: `sudo apt install docker.io docker-compose`

### 2. **Zbuduj APK jedną komendą**
```bash
# W folderze projektu
docker-compose up --build
```

### 3. **Alternatywnie użyj skryptu**
```bash
# Linux/Mac/WSL
chmod +x scripts/build.sh
./scripts/build.sh

# Windows PowerShell
docker-compose up --build
```

## 📁 **Co się dzieje podczas budowania:**

1. **Docker tworzy środowisko** Ubuntu z wszystkimi zależnościami
2. **Buildozer pobiera** Android SDK, NDK, Gradle
3. **Kompiluje aplikację** do pliku APK
4. **APK zapisuje się** w folderze `bin/`

## 🎯 **Wynik:**
```
bin/
└── zleceniapro-1.0-debug.apk  ← Twoja aplikacja!
```

## ⚡ **Szybkie komendy:**

### Podstawowe budowanie
```bash
docker-compose up
```

### Budowanie z czystym cache
```bash
docker-compose build --no-cache
docker-compose up
```

### Budowanie release (podpisanego)
```bash
# Najpierw edytuj buildozer.spec - dodaj keystore
docker-compose run android-builder buildozer android release
```

### Czyszczenie
```bash
docker-compose down
docker system prune
```

## 🔧 **Konfiguracja (buildozer.spec):**

Możesz edytować `buildozer.spec` aby zmienić:
- **Nazwę aplikacji** (`title`)
- **Identyfikator pakietu** (`package.domain`)  
- **Wersję** (`version`)
- **Ikony** (`icon.filename`)
- **Uprawnienia** (`android.permissions`)

## 🐛 **Troubleshooting:**

### Problem z prawami dostępu (Linux)
```bash
sudo chown -R $USER:$USER .buildozer/
sudo chown -R $USER:$USER bin/
```

### Brak miejsca na dysku
```bash
docker system prune -a
```

### Błędy SDK/NDK
```bash
# Usuń cache i zbuduj ponownie
docker-compose down -v
docker-compose up --build
```

### Sprawdź logi
```bash
docker-compose logs android-builder
```

## 📊 **Wymagania systemu:**

- **RAM:** 8GB+ (budowanie Android wymaga dużo pamięci)
- **Dysk:** 10GB+ wolnego miejsca
- **Internet:** Szybkie (pobiera ~2GB dependencies)
- **Czas:** 15-45 minut (pierwsze budowanie)

## 🎉 **Po zbudowaniu:**

1. **Skopiuj APK** na telefon Android
2. **Włącz "Nieznane źródła"** w ustawieniach
3. **Zainstaluj** przez menedżer plików
4. **Ciesz się** aplikacją! 🎯

---

## 📋 **GitHub Actions (opcjonalne)**

Możesz też użyć automatycznego budowania w chmurze - wyślij kod na GitHub i APK zbuduje się automatycznie!