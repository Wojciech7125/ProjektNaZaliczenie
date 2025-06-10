from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class RegisterScreen(BaseScreen):
    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Rejestracja",
            left_action=["arrow-left", lambda x: self.change_screen('login')]
        )

        # Formularz rejestracji
        scroll = ScrollView()
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            adaptive_height=True,
            padding=[dp(20), dp(20), dp(20), dp(20)]
        )

        # Logo
        logo_card = MDCard(
            size_hint=(1, None),
            height=dp(80),
            md_bg_color=self.app.get_color('secondary') if self.app else "#064653",
            elevation=2
        )

        logo_text = MDLabel(
            text="⚡ ZLECENIA PRO",
            font_style="H5",
            halign="center",
            theme_text_color="Primary"
        )
        logo_card.add_widget(logo_text)

        # Pola formularza
        self.reg_login = MDTextField(
            hint_text="Login *",
            icon_right="account"
        )

        self.reg_email = MDTextField(
            hint_text="Email *",
            icon_right="email"
        )

        self.reg_phone = MDTextField(
            hint_text="Numer Telefonu",
            icon_right="phone"
        )

        self.reg_company = MDTextField(
            hint_text="Nazwa Firmy *",
            icon_right="domain"
        )

        self.reg_specialization = MDTextField(
            hint_text="Specjalizacja *",
            icon_right="hammer-wrench"
        )

        self.reg_password = MDTextField(
            hint_text="Hasło *",
            icon_right="eye-off",
            password=True
        )

        self.reg_password_confirm = MDTextField(
            hint_text="Powtórz Hasło *",
            icon_right="eye-off",
            password=True
        )

        # Info o wymaganych polach
        info_label = MDLabel(
            text="* - pola wymagane",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )

        # Przyciski
        register_btn = MDRaisedButton(
            text="ZAREJESTRUJ SIĘ",
            size_hint_y=None,
            height=dp(48),
            on_release=self.register_user
        )

        back_btn = MDFlatButton(
            text="WRÓĆ",
            size_hint_y=None,
            height=dp(36),
            on_release=lambda x: self.change_screen('login')
        )

        # Dodaj wszystko do layoutu
        form_layout.add_widget(logo_card)
        form_layout.add_widget(self.reg_login)
        form_layout.add_widget(self.reg_email)
        form_layout.add_widget(self.reg_phone)
        form_layout.add_widget(self.reg_company)
        form_layout.add_widget(self.reg_specialization)
        form_layout.add_widget(self.reg_password)
        form_layout.add_widget(self.reg_password_confirm)
        form_layout.add_widget(info_label)
        form_layout.add_widget(register_btn)
        form_layout.add_widget(back_btn)

        scroll.add_widget(form_layout)

        main_layout = MDBoxLayout(orientation='vertical')
        main_layout.add_widget(top_bar)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def register_user(self, *args):
        """Rejestracja nowego użytkownika"""
        # Pobierz dane z formularza
        login = self.reg_login.text.strip()
        email = self.reg_email.text.strip()
        phone = self.reg_phone.text.strip()
        company = self.reg_company.text.strip()
        specialization = self.reg_specialization.text.strip()
        password = self.reg_password.text.strip()
        password_confirm = self.reg_password_confirm.text.strip()

        # Walidacja
        if not all([login, email, company, specialization, password, password_confirm]):
            self.show_error("Błąd", "Wypełnij wszystkie wymagane pola (oznaczone *)")
            return

        if len(password) < 6:
            self.show_error("Błąd", "Hasło musi mieć co najmniej 6 znaków")
            return

        if password != password_confirm:
            self.show_error("Błąd", "Hasła nie są identyczne")
            return

        if "@" not in email:
            self.show_error("Błąd", "Podaj prawidłowy adres email")
            return

        # Sprawdź czy użytkownik już istnieje
        data_manager = self.get_data_manager()
        if data_manager.user_exists(login):
            self.show_error("Błąd", "Użytkownik o tym loginie już istnieje")
            return

        # Dodaj użytkownika
        user_data = {
            'email': email,
            'phone': phone,
            'company': company,
            'specialization': specialization,
            'password': password
        }

        data_manager.add_user(login, user_data)
        self.show_dialog("Sukces", "Konto zostało utworzone",
                         callback=lambda: self.change_screen('login'))

        # Wyczyść formularz
        self.clear_form()

    def clear_form(self):
        """Wyczyść formularz"""
        self.reg_login.text = ""
        self.reg_email.text = ""
        self.reg_phone.text = ""
        self.reg_company.text = ""
        self.reg_specialization.text = ""
        self.reg_password.text = ""
        self.reg_password_confirm.text = ""