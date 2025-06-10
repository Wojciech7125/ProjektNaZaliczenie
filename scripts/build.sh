#!/bin/bash

# Skrypt do budowania aplikacji Android
set -e

echo "🔧 Zlecenia Pro - Android Build Script"
echo "====================================="

# Sprawdź czy Docker jest dostępny
if ! command -v docker &> /dev/null; then
    echo "❌ Docker nie jest zainstalowany!"
    echo "Zainstaluj Docker z: https://www.docker.com/get-started"
    exit 1
fi

# Sprawdź czy docker-compose jest dostępny
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose nie jest dostępny!"
    echo "Zainstaluj docker-compose"
    exit 1
fi

echo "📦 Budowanie obrazu Docker..."
docker-compose build

echo "🚀 Rozpoczynam budowanie APK..."
docker-compose up

echo "📱 Sprawdzanie wyników..."
if [ -f "bin/zleceniapro-*-debug.apk" ]; then
    echo "✅ APK został zbudowany pomyślnie!"
    echo "📍 Lokalizacja: $(ls bin/*.apk)"
    echo "📊 Rozmiar: $(du -h bin/*.apk | cut -f1)"
else
    echo "❌ Nie znaleziono pliku APK"
    echo "🔍 Sprawdź logi powyżej dla błędów"
fi

echo ""
echo "🎯 Gotowe! Możesz zainstalować APK na telefonie."