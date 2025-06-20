# 📱 Zlecenia Pro - Wojciech Wojtach

## 📁 Struktura folderów

```
zlecenia_pro/
├── main.py                    # Główny plik aplikacji
├── buildozer.spec            # Konfiguracja Android
├── requirements.txt          # Zależności Python
├── 
├── utils/                    # Narzędzia pomocnicze
│   ├── __init__.py
│   ├── data_manager.py       # Zarządzanie danymi
│   └── dialog_manager.py     # Zarządzanie dialogami
│
├── screens/                  # Ekrany aplikacji
│   ├── __init__.py
│   ├── base_screen.py        # Bazowy ekran
│   ├── login_screen.py       # Logowanie
│   ├── register_screen.py    # Rejestracja
│   ├── main_screen.py        # Główny dashboard
│   ├── projects_screen.py    # Lista projektów
│   ├── new_project_screen.py # Nowy projekt
│   ├── friends_screen.py     # Znajomi
│   ├── groups_screen.py      # Grupy
│   └── profile_screen.py     # Profil użytkownika
│
└── data/                     # Dane aplikacji (tworzone automatycznie)
    ├── users.json           # Użytkownicy
    ├── projects.json        # Projekty/zlecenia
    ├── groups.json          # Grupy
    └── friends.json         # Znajomi
```

## 🚀 Jak uruchomić

### 1. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 2. Uruchomienie na komputerze
```bash
python main.py
```

### 3. Budowanie APK dla Android
```bash
# Pierwsza instalacja buildozer
pip install buildozer

# Budowanie APK
buildozer android debug
```

## 🧩 Architektura komponentowa

### **Zalety modułowej struktury:**

✅ **Łatwe utrzymanie** - każdy ekran w osobnym pliku  
✅ **Ponowne użycie** - wspólna klasa BaseScreen  
✅ **Separacja logiki** - DataManager i DialogManager  
✅ **Skalowalne** - łatwe dodawanie nowych funkcji  
✅ **Czytelne** - logiczne podziały kodu  

### **Główne komponenty:**

- **main.py** - punkt wejścia, konfiguracja aplikacji
- **base_screen.py** - wspólne funkcje dla wszystkich ekranów
- **data_manager.py** - obsługa danych JSON, CRUD operations
- **dialog_manager.py** - okna dialogowe, powiadomienia
- **Screens** - poszczególne ekrany z własną logiką

## 📊 Model danych

### **users.json**
```json
{
  "username": {
    "email": "email@example.com",
    "phone": "+48123456789", 
    "company": "Firma ABC",
    "specialization": "Hydraulik",
    "password": "hashedpassword",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

### **projects.json**
```json
{
  "proj_1": {
    "name": "Remont łazienki",
    "location": "Warszawa",
    "description": "Kompleksowy remont",
    "budget": "5000",
    "author": "username",
    "status": "active",
    "recipients": ["user1", "user2"],
    "offers": [],
    "created_at": "2025-01-01T00:00:00"
  }
}
```

## 🔧 Dodawanie nowych funkcji

### Nowy ekran:
1. Utwórz `screens/new_screen.py`
2. Dziedzicz po `BaseScreen`
3. Dodaj do `main.py` w `build()`

### Nowa funkcja w DataManager:
1. Dodaj metodę w `data_manager.py`
2. Użyj w odpowiednim ekranie

### Nowy dialog:
1. Dodaj metodę w `dialog_manager.py`
2. Wywołaj z dowolnego ekranu

## 🎨 Customizacja

### Zmiana kolorów:
```python
# W main.py
self.theme_cls.primary_palette = "Blue"  # Zmień kolor główny
self.theme_cls.theme_style = "Light"     # Jasny motyw
```

### Dodanie nowych pól:
1. Zaktualizuj model w DataManager
2. Dodaj pola w odpowiednich formularzach
3. Zaktualizuj walidację

## 📱 Funkcjonalności

- ✅ **Logowanie/rejestracja** z walidacją
- ✅ **Dashboard** z statystykami
- ✅ **Tworzenie zleceń** z budżetem
- ✅ **Znajomi** - dodawanie, usuwanie
- ✅ **Grupy** - tworzenie, dołączanie
- ✅ **Profil** - edycja danych
- ✅ **Wyszukiwanie** projektów i użytkowników
- ✅ **Oferty** - składanie wycen
- ✅ **Filtrowanie** projektów

## 🔄 Możliwe rozszerzenia

- 💬 **Chat** między użytkownikami
- 📸 **Zdjęcia** w projektach
- 🗺️ **Mapa** lokalizacji
- 📊 **Wykresy** statystyk
- 🔔 **Push notifications**
- 💳 **Integracja płatności**
- 🌐 **API backend**
- 📱 **Synchronizacja** między urządzeniami
