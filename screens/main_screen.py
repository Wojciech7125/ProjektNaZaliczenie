from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, ThreeLineListItem
from utils.theme_helper import ThemeHelper
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class MainScreen(BaseScreen):
    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Dashboard",
            right_actions=[["bell", lambda x: self.show_notifications()]]
        )

        # Główna zawartość
        scroll = ScrollView()
        main_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            adaptive_height=True
        )

        # Sekcja witalna
        welcome_card = self.create_welcome_card()

        # Statystyki
        stats_layout = self.create_stats_section()

        # Szybkie akcje
        actions_section = self.create_actions_section()

        # Ostatnie zlecenia
        recent_section = self.create_recent_projects_section()

        # Dodaj wszystko do głównego layoutu
        main_content.add_widget(welcome_card)
        main_content.add_widget(stats_layout)
        main_content.add_widget(actions_section)
        main_content.add_widget(recent_section)

        scroll.add_widget(main_content)

        # Bottom navigation
        bottom_nav = self.create_bottom_navigation()

        # Layout główny
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(top_bar)
        layout.add_widget(scroll)
        layout.add_widget(bottom_nav)

        self.add_widget(layout)

    def create_welcome_card(self):
        """Karta powitalna"""
        welcome_card = ThemeHelper.create_themed_card(
            size_hint=(1, None),
            height=dp(100),
            elevation=0  # Wyłącz całkowicie cień
        )

        welcome_layout = MDBoxLayout(orientation='vertical')

        current_user = self.get_current_user()
        user_data = self.get_data_manager().get_user(current_user) if current_user else {}

        welcome_title = MDLabel(
            text=f"Witaj, {user_data.get('company', current_user) if current_user else 'Użytkowniku'}!",
            font_style="H6",
            theme_text_color="Primary"
        )

        welcome_subtitle = MDLabel(
            text=f"Specjalizacja: {user_data.get('specialization', 'Nie podano')}",
            font_style="Caption",
            theme_text_color="Secondary"
        )

        welcome_layout.add_widget(welcome_title)
        welcome_layout.add_widget(welcome_subtitle)
        welcome_card.add_widget(welcome_layout)

        return welcome_card

    def create_stats_section(self):
        """Sekcja statystyk"""
        stats_layout = MDGridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )

        current_user = self.get_current_user()
        if current_user:
            stats = self.get_data_manager().get_user_stats(current_user)

            active_card = self.create_stat_card(
                "Aktywne Zlecenia",
                str(stats.get('active_projects', 0)),
                "briefcase"
            )

            completed_card = self.create_stat_card(
                "Ukończone",
                str(stats.get('completed_projects', 0)),
                "check-circle"
            )
        else:
            active_card = self.create_stat_card("Aktywne Zlecenia", "0", "briefcase")
            completed_card = self.create_stat_card("Ukończone", "0", "check-circle")

        stats_layout.add_widget(active_card)
        stats_layout.add_widget(completed_card)

        return stats_layout

    def create_stat_card(self, title, value, icon):
        """Karta statystyki"""
        card = ThemeHelper.create_themed_card(
            elevation=0  # Wyłącz całkowicie cień
        )

        layout = MDBoxLayout(orientation='vertical')

        icon_label = MDLabel(
            text=icon,  # Uproszczone - można dodać faktyczne ikony
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )

        value_label = MDLabel(
            text=value,
            font_style="H6",
            halign="center",
            theme_text_color="Primary"
        )

        title_label = MDLabel(
            text=title,
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary"
        )

        layout.add_widget(icon_label)
        layout.add_widget(value_label)
        layout.add_widget(title_label)

        card.add_widget(layout)
        return card

    def create_actions_section(self):
        """Sekcja szybkich akcji"""
        actions_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(150)
        )

        actions_label = MDLabel(
            text="Szybkie akcje",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )

        buttons_layout = MDGridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(100)
        )

        new_project_btn = ThemeHelper.create_primary_button(
            "NOWE ZLECENIE",
            on_release=lambda x: self.change_screen('new_project')
        )

        browse_projects_btn = ThemeHelper.create_secondary_button(
            "PRZEGLĄDAJ ZLECENIA",
            on_release=lambda x: self.change_screen('projects')
        )

        buttons_layout.add_widget(new_project_btn)
        buttons_layout.add_widget(browse_projects_btn)

        actions_layout.add_widget(actions_label)
        actions_layout.add_widget(buttons_layout)

        return actions_layout

    def create_recent_projects_section(self):
        """Sekcja ostatnich projektów"""
        recent_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(300)
        )

        recent_label = MDLabel(
            text="Ostatnie zlecenia",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )

        recent_list = self.create_recent_projects_list()

        recent_layout.add_widget(recent_label)
        recent_layout.add_widget(recent_list)

        return recent_layout

    def create_recent_projects_list(self):
        """Lista ostatnich projektów"""
        list_widget = MDList()

        current_user = self.get_current_user()
        if current_user:
            projects = self.get_data_manager().get_projects_by_user(current_user)
            recent_projects = sorted(projects, key=lambda x: x.get('created_at', ''), reverse=True)[:3]

            for project in recent_projects:
                item = ThreeLineListItem(
                    text=project.get('name', 'Bez nazwy'),
                    secondary_text=project.get('location', 'Brak lokalizacji'),
                    tertiary_text=f"Budżet: {project.get('budget', 'Nie podano')}",
                    on_release=lambda x, p=project: self.show_project_details(p)
                )
                list_widget.add_widget(item)

        if not list_widget.children:
            # Dodaj placeholder jeśli brak projektów
            placeholder = MDLabel(
                text="Brak ostatnich zleceń",
                halign="center",
                theme_text_color="Secondary"
            )
            list_widget.add_widget(placeholder)

        return list_widget

    def show_project_details(self, project):
        """Pokaż szczegóły projektu"""
        if self.app:
            self.app.dialog_manager.show_project_details_dialog(project, self.app)

    def show_notifications(self, *args):
        """Pokaż powiadomienia"""
        self.show_dialog("Powiadomienia", "Brak nowych powiadomień")