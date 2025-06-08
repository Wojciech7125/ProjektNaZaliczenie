from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget


class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing='20dp',
            adaptive_height=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, None)
        )

        # Dodanie przestrzeni na górze
        main_layout.add_widget(Widget(size_hint_y=0.2))

        # Logo placeholder (trójkąt, kwadrat, koło)
        logo_card = MDCard(
            size_hint=(1, None),
            height='100dp',
            elevation=0,
            md_bg_color=(0.8, 0.8, 0.8, 1),
            radius=[15],
            pos_hint={'center_x': 0.5}
        )

        logo_layout = MDBoxLayout(
            orientation='horizontal',
            spacing='20dp',
            adaptive_height=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Symbole geometryczne jako placeholder
        triangle = MDLabel(
            text="▲",
            font_size='30sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        square = MDLabel(
            text="■",
            font_size='30sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        circle = MDLabel(
            text="●",
            font_size='30sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        logo_layout.add_widget(triangle)
        logo_layout.add_widget(square)
        logo_layout.add_widget(circle)
        logo_card.add_widget(logo_layout)

        main_layout.add_widget(logo_card)

        # Formularz rejestracji
        form_card = MDCard(
            size_hint=(1, None),
            height='450dp',
            elevation=3,
            md_bg_color=(0.149, 0.267, 0.298, 1),
            radius=[15],
            padding='20dp'
        )

        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing='15dp',
            adaptive_height=True
        )

        # Pole loginu
        self.login_field = MDTextField(
            hint_text="Login",
            size_hint_y=None,
            height='48dp',
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Pole email
        self.email_field = MDTextField(
            hint_text="Email",
            size_hint_y=None,
            height='48dp',
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Pole numeru telefonu
        self.phone_field = MDTextField(
            hint_text="Numer Telefonu",
            size_hint_y=None,
            height='48dp',
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Pole hasła
        self.password_field = MDTextField(
            hint_text="Hasło",
            password=True,
            size_hint_y=None,
            height='48dp',
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Pole potwierdzenia hasła
        self.confirm_password_field = MDTextField(
            hint_text="Powtórz Hasło",
            password=True,
            size_hint_y=None,
            height='48dp',
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Przycisk zarejestruj się
        register_button = MDRaisedButton(
            text="Zarejestruj się",
            size_hint_y=None,
            height='48dp',
            md_bg_color=(1, 0.5, 0, 1),
            on_release=self.register
        )

        # Przycisk wróć
        back_button = MDTextButton(
            text="Wróć",
            size_hint_y=None,
            height='48dp',
            theme_text_color="Custom",
            text_color=(1, 0.5, 0, 1),
            on_release=self.go_back
        )

        form_layout.add_widget(self.login_field)
        form_layout.add_widget(self.email_field)
        form_layout.add_widget(self.phone_field)
        form_layout.add_widget(self.password_field)
        form_layout.add_widget(self.confirm_password_field)
        form_layout.add_widget(Widget(size_hint_y=None, height='10dp'))
        form_layout.add_widget(register_button)
        form_layout.add_widget(back_button)

        form_card.add_widget(form_layout)
        main_layout.add_widget(form_card)

        # Dodanie przestrzeni na dole
        main_layout.add_widget(Widget(size_hint_y=0.2))

        self.add_widget(main_layout)

    def register(self, *args):
        # Prosta walidacja
        if (self.login_field.text and self.email_field.text and
                self.phone_field.text and self.password_field.text and
                self.password_field.text == self.confirm_password_field.text):
            self.manager.current = 'login'

    def go_back(self, *args):
        self.manager.current = 'login'