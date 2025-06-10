from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.metrics import dp


class LoginScreen(BaseScreen):
    def build_screen(self):
        # Logo
        logo_card = MDCard(
            size_hint=(0.8, None),
            height=dp(120),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            md_bg_color=self.app.theme_cls.primary_light if self.app else "orange",
            elevation=3
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
            height=dp(300),
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

        login_btn = MDRaisedButton(
            text="ZALOGUJ",
            size_hint_y=None,
            height=dp(48),
            on_release=self.login_user
        )

        register_btn = MDRaisedButton(
            text="ZAREJESTRUJ SIĘ",
            theme_icon_color="Custom",
            md_bg_color=self.app.theme_cls.primary_dark if self.app else "darkorange",
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self.change_screen('register')
        )

        forgot_btn = MDFlatButton(
            text="Zapomniałem hasła...",
            size_hint_y=None,
            height=dp(36),
            on_release=self.forgot_password
        )

        form_layout.add_widget(self.login_field)
        form_layout.add_widget(self.password_field)
        form_layout.add_widget(login_btn)
        form_layout.add_widget(register_btn)
        form_layout.add_widget(forgot_btn)

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
        else:
            self.show_error("Błąd", "Nieprawidłowy login lub hasło")

    def forgot_password(self, *args):
        """Obsługa zapomnienia hasła"""
        self.show_dialog("Informacja", "Funkcja resetowania hasła będzie dostępna wkrótce")

    def clear_form(self):
        """Wyczyść formularz"""
        self.login_field.text = ""
        self.password_field.text = ""