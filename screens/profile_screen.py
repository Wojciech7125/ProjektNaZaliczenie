from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class ProfileScreen(BaseScreen):
    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Profil",
            left_action=["arrow-left", lambda x: self.change_screen('main')],
            right_actions=[["pencil", lambda x: self.show_edit_profile_dialog()]]
        )

        scroll = ScrollView()
        profile_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            adaptive_height=True,
            padding=dp(20)
        )

        # Header z avatarem i podstawowymi info
        header_card = self.create_header_card()

        # Statystyki
        stats_card = self.create_stats_card()

        # Kontakt
        contact_card = self.create_contact_card()

        # Akcje profilu
        actions_card = self.create_actions_card()

        # Dodaj wszystko do profilu
        profile_layout.add_widget(header_card)
        profile_layout.add_widget(stats_card)
        profile_layout.add_widget(contact_card)
        profile_layout.add_widget(actions_card)

        scroll.add_widget(profile_layout)

        # Bottom navigation
        bottom_nav = self.create_bottom_navigation()

        # Layout główny
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(top_bar)
        layout.add_widget(scroll)
        layout.add_widget(bottom_nav)

        self.add_widget(layout)

    def create_header_card(self):
        """Karta header z podstawowymi informacjami"""
        header_card = MDCard(
            size_hint=(1, None),
            height=dp(150),
            padding=dp(15),
            elevation=3
        )

        header_layout = MDBoxLayout(orientation='horizontal', spacing=dp(20))

        # Avatar
        avatar_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=dp(80)
        )

        avatar_icon = MDIconButton(
            icon="account-circle",
            icon_size=dp(80),
            theme_icon_color="Custom",
            icon_color=self.app.theme_cls.primary_color if self.app else "orange"
        )

        avatar_layout.add_widget(avatar_icon)

        # Informacje użytkownika
        info_layout = MDBoxLayout(orientation='vertical')

        current_user = self.get_current_user()
        user_data = self.get_data_manager().get_user(current_user) if current_user else {}

        company = user_data.get('company', current_user if current_user else 'Użytkownik')
        specialization = user_data.get('specialization', 'Nie podano')

        user_name = MDLabel(
            text=company,
            font_style="H5",
            theme_text_color="Primary"
        )

        user_login = MDLabel(
            text=f"@{current_user}" if current_user else "@nieznany",
            font_style="Body2",
            theme_text_color="Secondary"
        )

        user_specialization = MDLabel(
            text=specialization,
            font_style="Caption",
            theme_text_color="Hint"
        )

        info_layout.add_widget(user_name)
        info_layout.add_widget(user_login)
        info_layout.add_widget(user_specialization)

        header_layout.add_widget(avatar_layout)
        header_layout.add_widget(info_layout)
        header_card.add_widget(header_layout)

        return header_card

    def create_stats_card(self):
        """Karta statystyk"""
        stats_card = MDCard(
            size_hint=(1, None),
            height=dp(120),
            padding=dp(15),
            elevation=2
        )

        stats_layout = MDGridLayout(cols=3, spacing=dp(10))

        current_user = self.get_current_user()
        if current_user:
            stats = self.get_data_manager().get_user_stats(current_user)

            projects_stat = self.create_profile_stat("Projekty", str(stats.get('sent_projects', 0)))
            friends_stat = self.create_profile_stat("Znajomi", str(stats.get('friends_count', 0)))
            completion_rate = round(stats.get('completion_rate', 0), 1)
            completed_stat = self.create_profile_stat("Ukończone", f"{completion_rate}%")
        else:
            projects_stat = self.create_profile_stat("Projekty", "0")
            friends_stat = self.create_profile_stat("Znajomi", "0")
            completed_stat = self.create_profile_stat("Ukończone", "0%")

        stats_layout.add_widget(projects_stat)
        stats_layout.add_widget(friends_stat)
        stats_layout.add_widget(completed_stat)

        stats_card.add_widget(stats_layout)
        return stats_card

    def create_profile_stat(self, title, value):
        """Pojedyncza statystyka profilu"""
        layout = MDBoxLayout(orientation='vertical')

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

        layout.add_widget(value_label)
        layout.add_widget(title_label)

        return layout

    def create_contact_card(self):
        """Karta informacji kontaktowych"""
        contact_card = MDCard(
            size_hint=(1, None),
            height=dp(120),
            padding=dp(15),
            elevation=2
        )

        contact_layout = MDBoxLayout(orientation='vertical', spacing=dp(5))

        contact_title = MDLabel(
            text="Informacje kontaktowe",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )

        current_user = self.get_current_user()
        user_data = self.get_data_manager().get_user(current_user) if current_user else {}

        email = user_data.get('email', 'Nie podano')
        phone = user_data.get('phone', 'Nie podano')

        email_label = MDLabel(
            text=f"📧 {email}",
            font_style="Body2",
            theme_text_color="Primary"
        )

        phone_label = MDLabel(
            text=f"📱 {phone}",
            font_style="Body2",
            theme_text_color="Primary"
        )

        contact_layout.add_widget(contact_title)
        contact_layout.add_widget(email_label)
        contact_layout.add_widget(phone_label)

        contact_card.add_widget(contact_layout)
        return contact_card

    def create_actions_card(self):
        """Karta z akcjami profilu"""
        actions_card = MDCard(
            size_hint=(1, None),
            height=dp(180),
            padding=dp(15),
            elevation=2
        )

        actions_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))

        actions_title = MDLabel(
            text="Akcje",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )

        edit_btn = MDRaisedButton(
            text="EDYTUJ PROFIL",
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.show_edit_profile_dialog()
        )

        settings_btn = MDFlatButton(
            text="USTAWIENIA",
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.show_settings()
        )

        logout_btn = MDFlatButton(
            text="WYLOGUJ",
            theme_text_color="Custom",
            text_color="red",
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.confirm_logout()
        )

        actions_layout.add_widget(actions_title)
        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(settings_btn)
        actions_layout.add_widget(logout_btn)

        actions_card.add_widget(actions_layout)
        return actions_card

    def show_edit_profile_dialog(self, *args):
        """Pokaż dialog edycji profilu"""
        if self.app:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.textfield import MDTextField
            from kivymd.uix.boxlayout import MDBoxLayout

            current_user = self.get_current_user()
            user_data = self.get_data_manager().get_user(current_user) if current_user else {}

            content = MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="300dp"
            )

            company_field = MDTextField(
                hint_text="Nazwa firmy",
                text=user_data.get('company', ''),
                size_hint_y=None,
                height="48dp"
            )

            specialization_field = MDTextField(
                hint_text="Specjalizacja",
                text=user_data.get('specialization', ''),
                size_hint_y=None,
                height="48dp"
            )

            email_field = MDTextField(
                hint_text="Email",
                text=user_data.get('email', ''),
                size_hint_y=None,
                height="48dp"
            )

            phone_field = MDTextField(
                hint_text="Telefon",
                text=user_data.get('phone', ''),
                size_hint_y=None,
                height="48dp"
            )

            content.add_widget(company_field)
            content.add_widget(specialization_field)
            content.add_widget(email_field)
            content.add_widget(phone_field)

            def save_profile():
                if not company_field.text.strip():
                    self.show_error("Błąd", "Podaj nazwę firmy")
                    return

                # Aktualizuj dane użytkownika
                updates = {
                    'company': company_field.text.strip(),
                    'specialization': specialization_field.text.strip(),
                    'email': email_field.text.strip(),
                    'phone': phone_field.text.strip()
                }

                # Zaktualizuj w danych
                user_data.update(updates)
                self.get_data_manager().users[current_user] = user_data
                self.get_data_manager().save_data(self.get_data_manager().users,
                                                  self.get_data_manager().users_file)

                self.show_dialog("Sukces", "Profil został zaktualizowany")

                # Odśwież ekran
                self.refresh_profile()

            dialog = MDDialog(
                title="Edytuj profil",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="ANULUJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="ZAPISZ",
                        on_release=lambda x: (dialog.dismiss(), save_profile())
                    )
                ]
            )
            dialog.open()

    def show_settings(self, *args):
        """Pokaż ustawienia"""
        self.show_dialog("Ustawienia", "Ustawienia aplikacji będą dostępne wkrótce")

    def confirm_logout(self, *args):
        """Potwierdź wylogowanie"""
        self.show_confirmation(
            "Wylogowanie",
            "Czy na pewno chcesz się wylogować?",
            self.logout
        )

    def logout(self, *args):
        """Wyloguj użytkownika"""
        if self.app:
            self.app.logout()

    def refresh_profile(self):
        """Odśwież dane profilu"""
        # Przebuduj ekran z nowymi danymi
        self.clear_widgets()
        self.build_screen()