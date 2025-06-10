from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class NewProjectScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_recipients = {
            'friends': False,
            'groups': False,
            'public': False
        }

    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Nowe Zlecenie",
            left_action=["arrow-left", lambda x: self.change_screen('projects')],
            right_actions=[["content-save", lambda x: self.save_draft()]]
        )

        # Formularz
        scroll = ScrollView()
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            adaptive_height=True,
            padding=dp(20)
        )

        # Podstawowe informacje
        basic_card = self.create_basic_info_card()

        # Szczegóły i budżet
        details_card = self.create_details_card()

        # Odbiorcy
        recipients_card = self.create_recipients_card()

        # Przyciski akcji
        actions_layout = self.create_actions_buttons()

        # Dodaj wszystko do formularza
        form_layout.add_widget(basic_card)
        form_layout.add_widget(details_card)
        form_layout.add_widget(recipients_card)
        form_layout.add_widget(actions_layout)

        scroll.add_widget(form_layout)

        # Layout główny
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(top_bar)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def create_basic_info_card(self):
        """Karta podstawowych informacji"""
        basic_card = MDCard(
            size_hint=(1, None),
            height=dp(320),
            padding=dp(15),
            elevation=2
        )

        basic_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))

        basic_title = MDLabel(
            text="Podstawowe informacje",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )

        self.project_name = MDTextField(
            hint_text="Nazwa projektu *",
            required=True
        )

        self.project_location = MDTextField(
            hint_text="Miejscowość *",
            required=True
        )

        self.project_area = MDTextField(
            hint_text="Powierzchnia (m²)",
            input_filter="float"
        )

        self.project_volume = MDTextField(
            hint_text="Objętość (m³)",
            input_filter="float"
        )

        basic_layout.add_widget(basic_title)
        basic_layout.add_widget(self.project_name)
        basic_layout.add_widget(self.project_location)
        basic_layout.add_widget(self.project_area)
        basic_layout.add_widget(self.project_volume)

        basic_card.add_widget(basic_layout)
        return basic_card

    def create_details_card(self):
        """Karta szczegółów"""
        details_card = MDCard(
            size_hint=(1, None),
            height=dp(220),
            padding=dp(15),
            elevation=2
        )

        details_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))

        details_title = MDLabel(
            text="Szczegóły i budżet",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )

        self.project_description = MDTextField(
            hint_text="Opis szczegółowy *",
            multiline=True,
            size_hint_y=None,
            height=dp(80),
            required=True
        )

        self.project_budget = MDTextField(
            hint_text="Budżet (PLN) *",
            input_filter="float",
            required=True
        )

        details_layout.add_widget(details_title)
        details_layout.add_widget(self.project_description)
        details_layout.add_widget(self.project_budget)

        details_card.add_widget(details_layout)
        return details_card

    def create_recipients_card(self):
        """Karta odbiorców"""
        recipients_card = MDCard(
            size_hint=(1, None),
            height=dp(180),
            padding=dp(15),
            elevation=2
        )

        recipients_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))

        recipients_title = MDLabel(
            text="Wyślij do:",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )

        # Opcje odbiorców z checkboxami
        options_layout = MDBoxLayout(orientation='vertical', spacing=dp(5))

        # Znajomi
        friends_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10))
        self.friends_checkbox = MDCheckbox(
            size_hint_x=None,
            width=dp(30),
            on_active=lambda checkbox, value: self.toggle_recipient('friends', value)
        )
        friends_label = MDLabel(text="Znajomi", size_hint_x=None, width=dp(100))
        friends_count = self.get_friends_count()
        friends_info = MDLabel(
            text=f"({friends_count} znajomych)",
            theme_text_color="Secondary"
        )

        friends_layout.add_widget(self.friends_checkbox)
        friends_layout.add_widget(friends_label)
        friends_layout.add_widget(friends_info)

        # Grupy
        groups_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10))
        self.groups_checkbox = MDCheckbox(
            size_hint_x=None,
            width=dp(30),
            on_active=lambda checkbox, value: self.toggle_recipient('groups', value)
        )
        groups_label = MDLabel(text="Grupy", size_hint_x=None, width=dp(100))
        groups_count = self.get_groups_count()
        groups_info = MDLabel(
            text=f"({groups_count} grup)",
            theme_text_color="Secondary"
        )

        groups_layout.add_widget(self.groups_checkbox)
        groups_layout.add_widget(groups_label)
        groups_layout.add_widget(groups_info)

        # Publiczne
        public_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10))
        self.public_checkbox = MDCheckbox(
            size_hint_x=None,
            width=dp(30),
            on_active=lambda checkbox, value: self.toggle_recipient('public', value)
        )
        public_label = MDLabel(text="Publiczne", size_hint_x=None, width=dp(100))
        public_info = MDLabel(
            text="(wszyscy użytkownicy)",
            theme_text_color="Secondary"
        )

        public_layout.add_widget(self.public_checkbox)
        public_layout.add_widget(public_label)
        public_layout.add_widget(public_info)

        options_layout.add_widget(friends_layout)
        options_layout.add_widget(groups_layout)
        options_layout.add_widget(public_layout)

        recipients_layout.add_widget(recipients_title)
        recipients_layout.add_widget(options_layout)

        recipients_card.add_widget(recipients_layout)
        return recipients_card

    def create_actions_buttons(self):
        """Przyciski akcji"""
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(48)
        )

        save_draft_btn = MDFlatButton(
            text="ZAPISZ SZKIC",
            on_release=lambda x: self.save_draft()
        )

        send_btn = MDRaisedButton(
            text="WYŚLIJ ZLECENIE",
            on_release=lambda x: self.send_project()
        )

        actions_layout.add_widget(save_draft_btn)
        actions_layout.add_widget(send_btn)

        return actions_layout

    def get_friends_count(self):
        """Pobierz liczbę znajomych"""
        current_user = self.get_current_user()
        if current_user:
            return len(self.get_data_manager().get_friends(current_user))
        return 0

    def get_groups_count(self):
        """Pobierz liczbę grup"""
        current_user = self.get_current_user()
        if current_user:
            return len(self.get_data_manager().get_groups_by_user(current_user))
        return 0

    def toggle_recipient(self, recipient_type, is_active):
        """Przełącz typ odbiorcy"""
        self.selected_recipients[recipient_type] = is_active

    def validate_form(self):
        """Waliduj formularz"""
        name = self.project_name.text.strip()
        location = self.project_location.text.strip()
        description = self.project_description.text.strip()
        budget = self.project_budget.text.strip()

        if not name:
            self.show_error("Błąd", "Podaj nazwę projektu")
            return False

        if not location:
            self.show_error("Błąd", "Podaj miejscowość")
            return False

        if not description:
            self.show_error("Błąd", "Podaj opis projektu")
            return False

        if not budget:
            self.show_error("Błąd", "Podaj budżet")
            return False

        # Sprawdź czy wybrano przynajmniej jeden typ odbiorcy
        if not any(self.selected_recipients.values()):
            self.show_error("Błąd", "Wybierz do kogo wysłać zlecenie")
            return False

        return True

    def get_project_data(self):
        """Pobierz dane projektu z formularza"""
        return {
            'name': self.project_name.text.strip(),
            'location': self.project_location.text.strip(),
            'area': self.project_area.text.strip(),
            'volume': self.project_volume.text.strip(),
            'description': self.project_description.text.strip(),
            'budget': self.project_budget.text.strip(),
            'author': self.get_current_user(),
            'recipients': self.get_recipients_list(),
            'visibility': 'public' if self.selected_recipients['public'] else 'private'
        }

    def get_recipients_list(self):
        """Pobierz listę odbiorców"""
        recipients = []
        current_user = self.get_current_user()

        if not current_user:
            return recipients

        data_manager = self.get_data_manager()

        # Dodaj znajomych
        if self.selected_recipients['friends']:
            friends = data_manager.get_friends(current_user)
            recipients.extend(friends)

        # Dodaj członków grup
        if self.selected_recipients['groups']:
            groups = data_manager.get_groups_by_user(current_user)
            for group in groups:
                group_data = data_manager.get_group(group['id'])
                if group_data:
                    members = group_data.get('members', [])
                    for member in members:
                        if member != current_user and member not in recipients:
                            recipients.append(member)

        return recipients

    def save_draft(self, *args):
        """Zapisz szkic"""
        if not self.project_name.text.strip():
            self.show_error("Błąd", "Podaj przynajmniej nazwę projektu")
            return

        project_data = self.get_project_data()
        project_data['status'] = 'draft'

        project_id = self.get_data_manager().add_project(project_data)

        self.show_dialog("Sukces", "Szkic zapisano",
                         callback=lambda: self.change_screen('projects'))
        self.clear_form()

    def send_project(self, *args):
        """Wyślij projekt"""
        if not self.validate_form():
            return

        project_data = self.get_project_data()
        project_data['status'] = 'active'

        project_id = self.get_data_manager().add_project(project_data)

        recipients_count = len(project_data['recipients'])
        if project_data['visibility'] == 'public':
            message = "Zlecenie zostało opublikowane publicznie"
        else:
            message = f"Zlecenie zostało wysłane do {recipients_count} odbiorców"

        self.show_dialog("Sukces", message,
                         callback=lambda: self.change_screen('projects'))
        self.clear_form()

    def clear_form(self):
        """Wyczyść formularz"""
        self.project_name.text = ""
        self.project_location.text = ""
        self.project_area.text = ""
        self.project_volume.text = ""
        self.project_description.text = ""
        self.project_budget.text = ""

        # Wyczyść checkboxy
        self.friends_checkbox.active = False
        self.groups_checkbox.active = False
        self.public_checkbox.active = False

        # Wyczyść stan odbiorców
        self.selected_recipients = {
            'friends': False,
            'groups': False,
            'public': False
        }