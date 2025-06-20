[app]
title = ZleceniaPro
package.name = zlecenia_pro
package.domain = org.example
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,json

# Możesz podać ścieżkę do ikony aplikacji, jeśli chcesz
# icon.filename = %(source.dir)s/icon.png

requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,plyer

orientation = portrait
fullscreen = 0
presplash.color = #000000

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b

# 👇 Kluczowe ustawienia zgodne z Java 8 i starszym Gradle
android.gradle_plugin_version = 4.2.2
android.gradle_wrapper_version = 6.7.1
android.javac = 1.8

# AndroidX
android.enable_androidx = True

# Format wyjściowy APK
android.release_artifact = aab
release.format = apk

# Wersje architektury (opcjonalnie możesz je ograniczyć)
# android.archs = armeabi-v7a, arm64-v8a

# Można włączyć logi adb jeśli trzeba
# logcat_filter = *

[buildozer]
log_level = 2
warn_on_root = 0
accept_sdk_license = True
android.accept_sdk_license = True

# (opcjonalne, jeśli masz timeouty przy pobieraniu)
# android.extra_repositories = https://dl.google.com/dl/android/maven2/

