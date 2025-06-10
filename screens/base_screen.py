from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


class BaseScreen(MDScreen):
    """Bazowa klasa dla wszystkich ekranów"""

    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_screen()

    def build_screen(self):
        """Metoda do przesłonięcia w klasach potomnych"""
        pass

    def create_top_bar(self, title, left_action=None, right_actions=None):
        """Stwórz górny pasek nawigacji"""
        left_actions = []
        if left_action:
            left_actions.append(left_action)

        right_action_items = []
        if right_actions:
            right_action_items = right_actions

        return MDTopAppBar(
            title=title,
            left_action_items=left_actions,
            right_action_items=right_action_items
        )

    def create_bottom_navigation(self):
        """Stwórz dolną nawigację"""
        bottom_nav = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            md_bg_color=self.app.theme_cls.primary_color if self.app else "orange"
        )

        # Przyciski nawigacji
        nav_buttons = [
            {"icon": "home", "text": "Główna", "screen": "main"},
            {"icon": "briefcase", "text": "Zlecenia", "screen": "projects"},
            {"icon": "account-group", "text": "Znajomi", "screen": "friends"},
            {"icon": "account-multiple", "text": "Grupy", "screen": "groups"},
            {"icon": "account", "text": "Profil", "screen": "profile"}
        ]

        for nav in nav_buttons:
            btn_layout = MDBoxLayout(
                orientation='vertical',
                size_hint_x=None,
                width=dp(80)
            )

            icon_btn = MDIconButton(
                icon=nav["icon"],
                theme_icon_color="Custom",
                icon_color="white",
                on_release=lambda x, screen=nav["screen"]: self.change_screen(screen)
            )

            label = MDLabel(
                text=nav["text"],
                font_style="Caption",
                halign="center",
                theme_text_color="Custom",
                text_color="white",
                size_hint_y=None,
                height=dp(15)
            )

            btn_layout.add_widget(icon_btn)
            btn_layout.add_widget(label)
            bottom_nav.add_widget(btn_layout)

        return bottom_nav

    def change_screen(self, screen_name):
        """Zmień ekran"""
        if self.app:
            self.app.change_screen(screen_name)

    def show_dialog(self, title, text, callback=None):
        """Pokaż dialog"""
        if self.app:
            self.app.dialog_manager.show_info_dialog(title, text, callback)

    def show_error(self, title, text, callback=None):
        """Pokaż błąd"""
        if self.app:
            self.app.dialog_manager.show_error_dialog(title, text, callback)

    def show_confirmation(self, title, text, on_confirm, on_cancel=None):
        """Pokaż potwierdzenie"""
        if self.app:
            self.app.dialog_manager.show_confirmation_dialog(title, text, on_confirm, on_cancel)

    def get_current_user(self):
        """Pobierz aktualnego użytkownika"""
        return self.app.get_current_user() if self.app else None

    def get_data_manager(self):
        """Pobierz data manager"""
        return self.app.data_manager if self.app else None