from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class Tab(MDFloatLayout, MDTabsBase):
    """Klasa tab dla MDTabs"""

    def __init__(self, **kwargs):
        # Usuń 'text' z kwargs przed przekazaniem do parent
        text = kwargs.pop('text', '')
        super().__init__(**kwargs)
        self.tab_label_text = text


class ProjectsScreen(BaseScreen):
    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Zlecenia",
            left_action=["arrow-left", lambda x: self.change_screen('main')],
            right_actions=[
                ["filter", lambda x: self.show_filters()],
                ["magnify", lambda x: self.show_search()]
            ]
        )

        # Tabs
        tabs = MDTabs()

        # Tab "Otrzymane"
        received_tab = Tab(text="Otrzymane")
        received_content = self.create_projects_list("received")
        received_tab.add_widget(received_content)
        tabs.add_widget(received_tab)

        # Tab "Wysłane"
        sent_tab = Tab(text="Wysłane")
        sent_content = self.create_projects_list("sent")
        sent_tab.add_widget(sent_content)
        tabs.add_widget(sent_tab)

        # FAB (Floating Action Button)
        fab = MDIconButton(
            icon="plus",
            theme_icon_color="Custom",
            icon_color="white",
            md_bg_color=self.app.get_color('primary') if self.app else "#ff7f00",
            pos_hint={'center_x': 0.9, 'center_y': 0.1},
            on_release=lambda x: self.change_screen('new_project')
        )

        # Layout główny
        content_layout = MDBoxLayout(orientation='vertical')
        content_layout.add_widget(top_bar)
        content_layout.add_widget(tabs)

        # Bottom navigation
        bottom_nav = self.create_bottom_navigation()
        content_layout.add_widget(bottom_nav)

        # Float layout dla FAB
        float_layout = MDFloatLayout()
        float_layout.add_widget(content_layout)
        float_layout.add_widget(fab)

        self.add_widget(float_layout)

    def create_projects_list(self, list_type):
        """Utwórz listę projektów"""
        scroll = ScrollView()
        list_widget = MDList()

        current_user = self.get_current_user()
        if current_user:
            data_manager = self.get_data_manager()

            if list_type == "received":
                # Projekty otrzymane - projekty innych użytkowników
                all_projects = []
                for project_id, project in data_manager.projects.items():
                    if project.get('author') != current_user:
                        # Sprawdź czy projekt jest publiczny lub skierowany do użytkownika
                        if (project.get('visibility') == 'public' or
                                current_user in project.get('recipients', [])):
                            all_projects.append({**project, 'id': project_id})

                projects = sorted(all_projects, key=lambda x: x.get('created_at', ''), reverse=True)

            else:  # sent
                # Projekty wysłane - projekty użytkownika
                projects = data_manager.get_projects_by_user(current_user, 'sent')
                projects = sorted(projects, key=lambda x: x.get('created_at', ''), reverse=True)

            for project in projects:
                if list_type == "received":
                    author_data = data_manager.get_user(project.get('author', ''))
                    author_name = author_data.get('company',
                                                  project.get('author', 'Nieznany')) if author_data else 'Nieznany'

                    item = ThreeLineListItem(
                        text=project.get('name', 'Bez nazwy'),
                        secondary_text=f"Od: {author_name}",
                        tertiary_text=f"{project.get('budget', 'Nie podano')} • {self.get_status_text(project.get('status', 'unknown'))}",
                        on_release=lambda x, p=project: self.show_project_details(p)
                    )
                else:  # sent
                    offers_count = len(project.get('offers', []))
                    offers_text = f"{offers_count} ofert" if offers_count != 1 else f"{offers_count} oferta"

                    item = ThreeLineListItem(
                        text=project.get('name', 'Bez nazwy'),
                        secondary_text=offers_text,
                        tertiary_text=f"{project.get('budget', 'Nie podano')} • {self.get_status_text(project.get('status', 'unknown'))}",
                        on_release=lambda x, p=project: self.show_project_details(p)
                    )

                list_widget.add_widget(item)

        # Jeśli brak projektów, dodaj placeholder
        if not list_widget.children:
            placeholder_text = ("Brak otrzymanych zleceń" if list_type == "received"
                                else "Nie wysłałeś jeszcze żadnych zleceń")

            placeholder = MDLabel(
                text=placeholder_text,
                halign="center",
                theme_text_color="Secondary",
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            list_widget.add_widget(placeholder)

        scroll.add_widget(list_widget)
        return scroll

    def get_status_text(self, status):
        """Pobierz tekst statusu w języku polskim"""
        status_map = {
            'active': 'Aktywne',
            'draft': 'Szkic',
            'in_progress': 'W trakcie',
            'completed': 'Zakończone',
            'cancelled': 'Anulowane',
            'unknown': 'Nieznany'
        }
        return status_map.get(status, 'Nieznany')

    def show_project_details(self, project):
        """Pokaż szczegóły projektu"""
        if self.app:
            self.app.dialog_manager.show_project_details_dialog(project, self.app)

    def show_filters(self, *args):
        """Pokaż opcje filtrowania"""
        if self.app:
            filter_options = [
                "Wszystkie",
                "Aktywne",
                "W trakcie",
                "Zakończone",
                "Budżet: do 1000 PLN",
                "Budżet: 1000-5000 PLN",
                "Budżet: powyżej 5000 PLN"
            ]

            self.app.dialog_manager.show_selection_dialog(
                "Filtry",
                filter_options,
                self.apply_filter
            )

    def apply_filter(self, selected_filter):
        """Zastosuj filtr"""
        self.show_dialog("Filtr", f"Zastosowano filtr: {selected_filter}")

    def show_search(self, *args):
        """Pokaż wyszukiwanie"""
        if self.app:
            self.app.dialog_manager.show_input_dialog(
                "Wyszukaj projekty",
                "Wpisz nazwę lub opis...",
                self.search_projects
            )

    def search_projects(self, query):
        """Wyszukaj projekty"""
        if query.strip():
            current_user = self.get_current_user()
            results = self.get_data_manager().search_projects(query, current_user)

            if results:
                results_text = f"Znaleziono {len(results)} projektów dla frazy: '{query}'"
            else:
                results_text = f"Nie znaleziono projektów dla frazy: '{query}'"

            self.show_dialog("Wyniki wyszukiwania", results_text)
        else:
            self.show_error("Błąd", "Wpisz frazę do wyszukania")