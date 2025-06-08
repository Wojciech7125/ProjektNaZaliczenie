from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.app import MDApp


class ProjectCreateScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [0.1, 0.3, 0.3, 1]  # Ciemny zielono-niebieski kolor tła

        main_layout = MDBoxLayout(
            orientation="vertical"
        )

        # Toolbar
        toolbar = MDTopAppBar(
            title="Nazwa Projektu",
            md_bg_color=[1, 0.5, 0, 1],  # Pomarańczowy
            specific_text_color=[1, 1, 1, 1],
            left_action_items=[["menu", lambda x: self.go_back()]],
            elevation=2
        )

        # Zawartość ekranu
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)]
        )

        # Lista opcji
        options = ["Miejsce", "Powierzchnia", "Prace"]

        for option in options:
            option_label = MDLabel(
                text=option,
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                size_hint_y=None,
                height=dp(40),
                font_style="H6"
            )
            content_layout.add_widget(option_label)

        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def go_back(self, *args):
        """Powrót do poprzedniego ekranu"""
        app = MDApp.get_running_app()
        app.go_to_screen('project_list')