from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget


class LoginScreen(MDScreen):
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
        main_layout.add_widget(Widget(size_hint_y=0.3))

        # Logo placeholder (trójkąt, kwadrat, koło)
        logo_card = MDCard(
            size_hint=(1, None),
            height='150dp',
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
            font_size='40sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        square = MDLabel(
            text="■",
            font_size='40sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        circle = MDLabel(
            text="●",
            font_size='40sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        logo_layout.add_widget(triangle)
        logo_layout.add_widget(square)
        logo_layout.add_widget(circle)
        logo_card.add_widget(logo_layout)

        main_layout.add_widget(logo_card)

        # Formularz logowania
        form_card = MDCard(
            size_hint=(1, None),
            height='350dp',
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

        # Pole hasła
        self.password_field = MDTextField(
            hint_text="********",
            password=True,
            size_hint_y=None,
            height='48dp',
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Przycisk zaloguj
        login_button = MDRaisedButton(
            text="Zaloguj",
            size_hint_y=None,
            height='48dp',
            md_bg_color=(1, 0.5, 0, 1),
            on_release=self.login
        )

        # Przycisk zarejestruj się
        register_button = MDRaisedButton(
            text="Zarejestruj się",
            size_hint_y=None,
            height='48dp',
            md_bg_color=(1, 0.5, 0, 1),
            on_release=self.go_to_register
        )

        # Label "Zapomniałem hasła..."
        forgot_password = MDLabel(
            text="Zapomniałem hasła...",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            halign="center",
            size_hint_y=None,
            height='30dp'
        )

        form_layout.add_widget(self.login_field)
        form_layout.add_widget(self.password_field)
        form_layout.add_widget(Widget(size_hint_y=None, height='10dp'))
        form_layout.add_widget(login_button)
        form_layout.add_widget(register_button)
        form_layout.add_widget(forgot_password)

        form_card.add_widget(form_layout)
        main_layout.add_widget(form_card)

        # Dodanie przestrzeni na dole
        main_layout.add_widget(Widget(size_hint_y=0.3))

        self.add_widget(main_layout)

    def login(self, *args):
        # Prosta walidacja - przejście do listy zamówień
        if self.login_field.text and self.password_field.text:
            self.manager.current = 'order_list'

    def go_to_register(self, *args):
        self.manager.current = 'register'