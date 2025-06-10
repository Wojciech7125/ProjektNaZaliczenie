from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class FriendsScreen(BaseScreen):
    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Znajomi",
            left_action=["arrow-left", lambda x: self.change_screen('main')],
            right_actions=[["account-plus", lambda x: self.show_add_friend_dialog()]]
        )

        # Search bar
        search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(56),
            padding=[dp(10), dp(5)]
        )

        self.friends_search = MDTextField(
            hint_text="Szukaj znajomych...",
            size_hint_x=0.8
        )

        search_btn = MDIconButton(
            icon="magnify",
            on_release=self.search_friends
        )

        search_layout.add_widget(self.friends_search)
        search_layout.add_widget(search_btn)

        # Lista znajomych
        self.friends_scroll = ScrollView()
        self.update_friends_list()

        # Bottom navigation
        bottom_nav = self.create_bottom_navigation()

        # Layout główny
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(top_bar)
        layout.add_widget(search_layout)
        layout.add_widget(self.friends_scroll)
        layout.add_widget(bottom_nav)

        self.add_widget(layout)

    def update_friends_list(self, search_query=""):
        """Zaktualizuj listę znajomych"""
        friends_list = MDList()

        current_user = self.get_current_user()
        if current_user:
            data_manager = self.get_data_manager()
            friends = data_manager.get_friends(current_user)

            # Filtruj znajomych jeśli jest zapytanie wyszukiwania
            if search_query:
                filtered_friends = []
                for friend_username in friends:
                    friend_data = data_manager.get_user(friend_username)
                    if friend_data:
                        name = friend_data.get('company', friend_username)
                        specialization = friend_data.get('specialization', '')
                        if (search_query.lower() in name.lower() or
                                search_query.lower() in specialization.lower() or
                                search_query.lower() in friend_username.lower()):
                            filtered_friends.append(friend_username)
                friends = filtered_friends

            # Dodaj znajomych do listy
            for friend_username in friends:
                friend_data = data_manager.get_user(friend_username)
                if friend_data:
                    item = self.create_friend_item(friend_username, friend_data)
                    friends_list.add_widget(item)

        # Jeśli brak znajomych, dodaj placeholder
        if not friends_list.children:
            placeholder_text = ("Brak znajomych pasujących do wyszukiwania" if search_query
                                else "Nie masz jeszcze znajomych")

            placeholder = MDLabel(
                text=placeholder_text,
                halign="center",
                theme_text_color="Secondary",
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            friends_list.add_widget(placeholder)

        # Wyczyść i dodaj nową listę
        self.friends_scroll.clear_widgets()
        self.friends_scroll.add_widget(friends_list)

    def create_friend_item(self, friend_username, friend_data):
        """Utwórz element listy znajomego"""
        company = friend_data.get('company', friend_username)
        specialization = friend_data.get('specialization', 'Brak specjalizacji')

        item = TwoLineListItem(
            text=company,
            secondary_text=specialization,
            on_release=lambda x: self.show_friend_profile(friend_username, friend_data)
        )

        # Dodaj przycisk do usuwania znajomego
        remove_btn = MDIconButton(
            icon="account-minus",
            theme_icon_color="Custom",
            icon_color="red",
            pos_hint={'center_y': 0.5, 'right': 1},
            on_release=lambda x: self.confirm_remove_friend(friend_username, company)
        )

        item.add_widget(remove_btn)
        return item

    def on_search_text_change(self, instance, text):
        """Obsługa zmiany tekstu w wyszukiwaniu"""
        # Opcjonalnie: wyszukiwanie w czasie rzeczywistym
        pass

    def search_friends(self, *args):
        """Wyszukaj znajomych"""
        search_text = self.friends_search.text.strip()
        self.update_friends_list(search_text)

    def show_add_friend_dialog(self, *args):
        """Pokaż dialog dodawania znajomego"""
        if self.app:
            self.app.dialog_manager.show_input_dialog(
                "Dodaj znajomego",
                "Wpisz login użytkownika...",
                self.add_friend
            )

    def add_friend(self, friend_username):
        """Dodaj znajomego"""
        friend_username = friend_username.strip()

        if not friend_username:
            self.show_error("Błąd", "Podaj login użytkownika")
            return

        current_user = self.get_current_user()
        data_manager = self.get_data_manager()

        # Sprawdź czy użytkownik istnieje
        if not data_manager.user_exists(friend_username):
            self.show_error("Błąd", "Użytkownik o podanym loginie nie istnieje")
            return

        # Sprawdź czy to nie ten sam użytkownik
        if friend_username == current_user:
            self.show_error("Błąd", "Nie możesz dodać siebie jako znajomego")
            return

        # Sprawdź czy już nie jest znajomym
        if data_manager.are_friends(current_user, friend_username):
            self.show_error("Błąd", "Ten użytkownik jest już Twoim znajomym")
            return

        # Dodaj znajomego
        data_manager.add_friend(current_user, friend_username)

        friend_data = data_manager.get_user(friend_username)
        company = friend_data.get('company', friend_username) if friend_data else friend_username

        self.show_dialog("Sukces", f"Dodano {company} do znajomych")

        # Odśwież listę
        self.update_friends_list()

    def confirm_remove_friend(self, friend_username, friend_name):
        """Potwierdź usunięcie znajomego"""
        self.show_confirmation(
            "Usuń znajomego",
            f"Czy na pewno chcesz usunąć {friend_name} ze znajomych?",
            lambda: self.remove_friend(friend_username)
        )

    def remove_friend(self, friend_username):
        """Usuń znajomego"""
        current_user = self.get_current_user()
        data_manager = self.get_data_manager()

        data_manager.remove_friend(current_user, friend_username)

        self.show_dialog("Sukces", "Znajomy został usunięty")

        # Odśwież listę
        self.update_friends_list()

    def show_friend_profile(self, friend_username, friend_data):
        """Pokaż profil znajomego"""
        company = friend_data.get('company', friend_username)
        specialization = friend_data.get('specialization', 'Brak specjalizacji')
        email = friend_data.get('email', 'Brak email')
        phone = friend_data.get('phone', 'Brak telefonu')

        profile_text = f"""
Firma: {company}
Specjalizacja: {specialization}
Email: {email}
Telefon: {phone}
        """.strip()

        if self.app:
            self.app.dialog_manager.show_info_dialog(
                f"Profil - {company}",
                profile_text
            )