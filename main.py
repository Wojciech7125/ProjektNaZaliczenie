from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


class MobileApp(MDApp):
    def build(self):
        # Symulacja rozmiaru ekranu mobilnego
        Window.size = (360, 640)  # Typowy rozmiar telefonu

        # Ustawienie motywu
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        # Główny ekran
        screen = MDScreen()

        # ScrollView dla przewijania zawartości
        scroll = ScrollView()

        # Layout główny - zoptymalizowany pod mobile
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            adaptive_height=True,
            padding=[dp(16), dp(20), dp(16), dp(16)]
        )

        # Header sekcja
        header_card = MDCard(
            size_hint=(1, None),
            height=dp(120),
            padding=dp(20),
            elevation=3,
            radius=[15],
            md_bg_color=[0.2, 0.6, 1, 0.1]
        )

        header_content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )

        app_title = MDLabel(
            text="📱 MobileApp",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )

        app_subtitle = MDLabel(
            text="Aplikacja mobilna w KivyMD",
            theme_text_color="Secondary",
            font_style="Subtitle1",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )

        # Status bar
        status_label = MDLabel(
            text="Status: Gotowa do użycia ✅",
            theme_text_color="Primary",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=dp(25)
        )

        # Główna karta funkcji
        main_card = MDCard(
            size_hint=(1, None),
            height=dp(200),
            padding=dp(20),
            elevation=5,
            radius=[15]
        )

        main_card_content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12)
        )

        card_title = MDLabel(
            text="💼 Panel główny",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(35)
        )

        card_description = MDLabel(
            text="Wprowadź tekst poniżej i użyj przycisków do testowania funkcji aplikacji. Wszystkie elementy są zoptymalizowane pod ekrany dotykowe.",
            theme_text_color="Secondary",
            text_size=(dp(280), None),
            halign="left",
            valign="top"
        )

        # Pole tekstowe - większe dla mobile
        self.text_field = MDTextField(
            hint_text="Wprowadź tekst tutaj...",
            helper_text="Dotknij, aby rozpocząć pisanie",
            helper_text_mode="persistent",
            size_hint_y=None,
            height=dp(70),
            mode="rectangle",
            font_size=dp(16)
        )

        # Sekcja przycisków - większe dla mobile
        buttons_label = MDLabel(
            text="🎮 Akcje:",
            font_style="Subtitle1",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )

        # Pierwszy rząd - większe przyciski
        button_row1 = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(60)
        )

        test_button = MDRaisedButton(
            text="Test tekstu",
            on_press=self.on_test_button_press,
            size_hint=(0.7, 1),
            font_size=dp(16)
        )

        heart_button = MDIconButton(
            icon="heart",
            theme_icon_color="Custom",
            icon_color="red",
            on_press=self.on_heart_button_press,
            size_hint=(0.3, 1),
            icon_size=dp(32)
        )

        # Drugi rząd przycisków
        button_row2 = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(60)
        )

        dialog_button = MDRaisedButton(
            text="Pokaż okno",
            on_press=self.show_dialog,
            size_hint=(0.5, 1),
            font_size=dp(16)
        )

        clear_button = MDRaisedButton(
            text="Wyczyść",
            on_press=self.clear_text_field,
            size_hint=(0.5, 1),
            font_size=dp(16)
        )

        # Trzeci rząd - dodatkowe funkcje
        button_row3 = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(60)
        )

        info_button = MDRaisedButton(
            text="📋 Info",
            on_press=self.show_info,
            size_hint=(0.5, 1),
            font_size=dp(16)
        )

        settings_button = MDRaisedButton(
            text="⚙️ Ustawienia",
            on_press=self.show_settings,
            size_hint=(0.5, 1),
            font_size=dp(16)
        )

        # Karta statystyk
        stats_card = MDCard(
            size_hint=(1, None),
            height=dp(100),
            padding=dp(16),
            elevation=3,
            radius=[10],
            md_bg_color=[0, 0.8, 0, 0.1]
        )

        stats_content = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20)
        )

        self.click_counter = 0
        self.stats_label = MDLabel(
            text=f"🎯 Kliknięcia: {self.click_counter}",
            theme_text_color="Primary",
            font_style="Subtitle1",
            halign="center"
        )

        # FAB - większy dla mobile
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.5},
            on_press=self.on_fab_press,
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )

        # Budowanie struktury
        header_content.add_widget(app_title)
        header_content.add_widget(app_subtitle)
        header_content.add_widget(status_label)
        header_card.add_widget(header_content)

        main_card_content.add_widget(card_title)
        main_card_content.add_widget(card_description)
        main_card.add_widget(main_card_content)

        button_row1.add_widget(test_button)
        button_row1.add_widget(heart_button)

        button_row2.add_widget(dialog_button)
        button_row2.add_widget(clear_button)

        button_row3.add_widget(info_button)
        button_row3.add_widget(settings_button)

        stats_content.add_widget(self.stats_label)
        stats_card.add_widget(stats_content)

        # Dodawanie do głównego layoutu
        main_layout.add_widget(header_card)
        main_layout.add_widget(main_card)
        main_layout.add_widget(self.text_field)
        main_layout.add_widget(buttons_label)
        main_layout.add_widget(button_row1)
        main_layout.add_widget(button_row2)
        main_layout.add_widget(button_row3)
        main_layout.add_widget(stats_card)
        main_layout.add_widget(fab)

        scroll.add_widget(main_layout)
        screen.add_widget(scroll)

        return screen

    def update_stats(self):
        """Aktualizuje licznik kliknięć"""
        self.click_counter += 1
        self.stats_label.text = f"🎯 Kliknięcia: {self.click_counter}"

    def on_test_button_press(self, instance):
        """Obsługa przycisku testowego"""
        self.update_stats()
        text = self.text_field.text if self.text_field.text else "Brak tekstu"
        self.show_snackbar(f"📝 Tekst: {text}")

    def on_heart_button_press(self, instance):
        """Obsługa przycisku serca"""
        self.update_stats()
        self.show_snackbar("❤️ Dzięki za kliknięcie!")

    def on_fab_press(self, instance):
        """Obsługa FAB"""
        self.update_stats()
        self.show_snackbar("🚀 FAB aktywowany!")

    def clear_text_field(self, instance):
        """Czyści pole tekstowe"""
        self.update_stats()
        self.text_field.text = ""
        self.show_snackbar("🗑️ Pole wyczyszczone")

    def show_info(self, instance):
        """Pokazuje informacje o aplikacji"""
        self.update_stats()
        dialog = MDDialog(
            title="📱 Informacje",
            text="Aplikacja mobilna stworzona w KivyMD\n\n• Zoptymalizowana pod ekrany dotykowe\n• Responsywny interfejs\n• Łatwa obsługa gestem\n\nWersja: 1.0.0",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def show_settings(self, instance):
        """Pokazuje ustawienia (przykład)"""
        self.update_stats()
        dialog = MDDialog(
            title="⚙️ Ustawienia",
            text="Panel ustawień aplikacji:\n\n• Motyw: Jasny\n• Język: Polski\n• Powiadomienia: Włączone\n• Dźwięki: Włączone\n\n(To jest przykład - funkcje do implementacji)",
            buttons=[
                MDRaisedButton(
                    text="Zapisz",
                    on_press=lambda x: self.save_settings(dialog)
                ),
                MDRaisedButton(
                    text="Anuluj",
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def save_settings(self, dialog):
        """Zapisuje ustawienia"""
        dialog.dismiss()
        self.show_snackbar("💾 Ustawienia zapisane!")

    def show_snackbar(self, text):
        """Pokazuje snackbar z wiadomością"""
        try:
            Snackbar(text=text).open()
        except Exception as e:
            print(f"Snackbar error: {e}")
            print(f"Wiadomość: {text}")

    def show_dialog(self, instance):
        """Pokazuje główne okno dialogowe"""
        self.update_stats()
        dialog = MDDialog(
            title="💬 Okno dialogowe",
            text="Witaj w aplikacji mobilnej!\n\nTo okno jest zoptymalizowane pod urządzenia mobilne z większymi przyciskami i lepszą czytelności.",
            buttons=[
                MDRaisedButton(
                    text="Anuluj",
                    on_press=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="OK",
                    on_press=lambda x: self.dialog_ok_pressed(dialog)
                )
            ]
        )
        dialog.open()

    def dialog_ok_pressed(self, dialog):
        """Obsługa OK w dialogu"""
        dialog.dismiss()
        self.show_snackbar("✅ Dialog zatwierdzony!")


# Uruchomienie aplikacji
if __name__ == "__main__":
    MobileApp().run()