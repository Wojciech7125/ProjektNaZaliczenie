from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from utils.theme_helper import ThemeHelper
from kivy.metrics import dp


class LoginScreen(BaseScreen):
    def build_screen(self):
        # Logo
        logo_card = ThemeHelper.create_themed_card(
            size_hint=(0.8, None),
            height=dp(120),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        logo_text = MDLabel(
            text="⚡ ZLECENIA PRO",
            font_style="H4",
            halign="center",
            theme_text_color="Primary",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        logo_card.add_widget(logo_text)

        # Formularz logowania
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint=(0.85, None),
            height=dp(380),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )

        self.login_field = MDTextField(
            hint_text="Login",
            icon_right="account",
            size_hint_y=None,
            height=dp(48)
        )

        self.password_field = MDTextField(
            hint_text="Hasło",
            icon_right="eye-off",
            password=True,
            size_hint_y=None,
            height=dp(48)
        )

        login_btn = ThemeHelper.create_primary_button(
            "ZALOGUJ",
            on_release=self.login_user
        )

        register_btn = ThemeHelper.create_secondary_button(
            "ZAREJESTRUJ SIĘ",
            on_release=lambda x: self.change_screen('register')
        )

        forgot_btn = ThemeHelper.create_flat_button(
            "Zapomniałem hasła...",
            on_release=self.forgot_password
        )

        # Info o kontach testowych
        demo_info = MDLabel(
            text="Konta testowe:\n• demo / demo123\n• test / test123",
            font_style="Caption",
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=None,
            height=dp(60)
        )

        form_layout.add_widget(self.login_field)
        form_layout.add_widget(self.password_field)
        form_layout.add_widget(login_btn)
        form_layout.add_widget(register_btn)
        form_layout.add_widget(forgot_btn)
        form_layout.add_widget(demo_info)

        # Główny layout dla ekranu
        main_layout = MDFloatLayout()
        main_layout.add_widget(logo_card)
        main_layout.add_widget(form_layout)

        self.add_widget(main_layout)

    def login_user(self, *args):
        """Logowanie użytkownika"""
        login = self.login_field.text.strip()
        password = self.password_field.text.strip()

        if not login or not password:
            self.show_error("Błąd", "Wypełnij wszystkie pola")
            return

        # Sprawdź dane logowania
        data_manager = self.get_data_manager()
        if data_manager and data_manager.validate_user(login, password):
            self.app.set_current_user(login)
            self.change_screen('main')
            self.clear_form()

            # Pokaż wiadomość powitalną
            user_data = data_manager.get_user(login)
            company = user_data.get('company', login) if user_data else login
            self.show_dialog("Witamy!", f"Zalogowano jako {company}")
        else:
            # Sprawdź czy użytkownik istnieje
            if data_manager and data_manager.user_exists(login):
                self.show_error("Błąd", "Nieprawidłowe hasło")
            else:
                self.show_error("Błąd",
                                f"Użytkownik '{login}' nie istnieje.\n\nSpróbuj:\n• demo / demo123\n• test / test123\n• lub zarejestruj się")

    def forgot_password(self, *args):
        """Obsługa zapomnienia hasła"""
        self.show_dialog("Informacja", "Funkcja resetowania hasła będzie dostępna wkrótce")

    def clear_form(self):
        """Wyczyść formularz"""
        self.login_field.text = ""
        self.password_field.text = ""