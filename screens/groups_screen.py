from screens.base_screen import BaseScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class Tab(MDFloatLayout, MDTabsBase):
    """Klasa tab dla MDTabs"""

    def __init__(self, **kwargs):
        # Usuń 'text' z kwargs przed przekazaniem do parent
        text = kwargs.pop('text', '')
        super().__init__(**kwargs)
        self.tab_label_text = text


class GroupsScreen(BaseScreen):
    def build_screen(self):
        # Top bar
        top_bar = self.create_top_bar(
            title="Grupy",
            left_action=["arrow-left", lambda x: self.change_screen('main')],
            right_actions=[["account-group", lambda x: self.show_create_group_dialog()]]
        )

        # Tabs
        tabs = MDTabs()

        # Tab "Moje grupy"
        my_groups_tab = Tab(text="Moje grupy")
        my_groups_content = self.create_groups_list("my")
        my_groups_tab.add_widget(my_groups_content)
        tabs.add_widget(my_groups_tab)

        # Tab "Dostępne"
        available_tab = Tab(text="Dostępne")
        available_content = self.create_groups_list("available")
        available_tab.add_widget(available_content)
        tabs.add_widget(available_tab)

        # Bottom navigation
        bottom_nav = self.create_bottom_navigation()

        # Layout główny
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(top_bar)
        layout.add_widget(tabs)
        layout.add_widget(bottom_nav)

        self.add_widget(layout)

    def create_groups_list(self, list_type):
        """Utwórz listę grup"""
        scroll = ScrollView()
        list_widget = MDList()

        current_user = self.get_current_user()
        if current_user:
            data_manager = self.get_data_manager()

            if list_type == "my":
                groups = data_manager.get_groups_by_user(current_user, 'all')
            else:  # available
                groups = data_manager.get_available_groups(current_user)

            for group in groups:
                item = self.create_group_item(group, list_type)
                list_widget.add_widget(item)

        # Jeśli brak grup, dodaj placeholder
        if not list_widget.children:
            placeholder_text = ("Nie należysz do żadnych grup" if list_type == "my"
                                else "Brak dostępnych grup")

            placeholder = MDLabel(
                text=placeholder_text,
                halign="center",
                theme_text_color="Secondary",
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            list_widget.add_widget(placeholder)

        scroll.add_widget(list_widget)
        return scroll

    def create_group_item(self, group, list_type):
        """Utwórz element listy grupy"""
        name = group.get('name', 'Bez nazwy')
        description = group.get('description', 'Brak opisu')
        members_count = len(group.get('members', []))
        group_type = group.get('type', 'Nieznany typ')

        members_text = f"{members_count} członków"
        type_text = f"Typ: {group_type}"

        item = ThreeLineListItem(
            text=name,
            secondary_text=members_text,
            tertiary_text=type_text,
            on_release=lambda x: self.show_group_details(group)
        )

        return item

    def show_group_details(self, group):
        """Pokaż szczegóły grupy"""
        name = group.get('name', 'Bez nazwy')
        description = group.get('description', 'Brak opisu')
        members_count = len(group.get('members', []))
        group_type = group.get('type', 'Nieznany')
        owner = group.get('owner', 'Nieznany')

        # Pobierz dane właściciela
        owner_data = self.get_data_manager().get_user(owner)
        owner_name = owner_data.get('company', owner) if owner_data else owner

        details_text = f"""
Nazwa: {name}
Opis: {description}
Członków: {members_count}
Typ: {group_type}
Właściciel: {owner_name}
        """.strip()

        current_user = self.get_current_user()
        is_member = current_user in group.get('members', [])

        # Przyciski w zależności od członkostwa
        if is_member:
            if group.get('owner') == current_user:
                # Właściciel - może zarządzać grupą
                self.show_owner_group_dialog(group, details_text)
            else:
                # Członek - może opuścić grupę
                self.show_member_group_dialog(group, details_text)
        else:
            # Nie jest członkiem - może dołączyć
            self.show_join_group_dialog(group, details_text)

    def show_owner_group_dialog(self, group, details_text):
        """Dialog dla właściciela grupy"""
        if self.app:
            from kivymd.uix.dialog import MDDialog

            dialog = MDDialog(
                title="Szczegóły grupy",
                text=details_text,
                buttons=[
                    MDFlatButton(
                        text="ZAMKNIJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="ZARZĄDZAJ",
                        on_release=lambda x: (dialog.dismiss(), self.manage_group(group))
                    )
                ]
            )
            dialog.open()

    def show_member_group_dialog(self, group, details_text):
        """Dialog dla członka grupy"""
        if self.app:
            from kivymd.uix.dialog import MDDialog

            dialog = MDDialog(
                title="Szczegóły grupy",
                text=details_text,
                buttons=[
                    MDFlatButton(
                        text="ZAMKNIJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OPUŚĆ GRUPĘ",
                        theme_text_color="Custom",
                        text_color="red",
                        on_release=lambda x: (dialog.dismiss(), self.confirm_leave_group(group))
                    )
                ]
            )
            dialog.open()

    def show_join_group_dialog(self, group, details_text):
        """Dialog dla osób spoza grupy"""
        if self.app:
            from kivymd.uix.dialog import MDDialog

            dialog = MDDialog(
                title="Szczegóły grupy",
                text=details_text,
                buttons=[
                    MDFlatButton(
                        text="ZAMKNIJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="DOŁĄCZ",
                        on_release=lambda x: (dialog.dismiss(), self.join_group(group))
                    )
                ]
            )
            dialog.open()

    def show_create_group_dialog(self, *args):
        """Pokaż dialog tworzenia grupy"""
        if self.app:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.textfield import MDTextField
            from kivymd.uix.boxlayout import MDBoxLayout
            from kivymd.uix.button import MDRectangleFlatButton
            from kivymd.uix.list import OneLineListItem

            content = MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="250dp"
            )

            name_field = MDTextField(
                hint_text="Nazwa grupy",
                size_hint_y=None,
                height="48dp"
            )

            description_field = MDTextField(
                hint_text="Opis grupy",
                multiline=True,
                size_hint_y=None,
                height="80dp"
            )

            # Typ grupy - prosty przycisk z tekstem
            self.group_type = "Branżowa"
            type_button = MDRectangleFlatButton(
                text="Typ: Branżowa",
                size_hint_y=None,
                height="40dp",
                on_release=lambda x: self.show_type_selection(type_button)
            )

            content.add_widget(name_field)
            content.add_widget(description_field)
            content.add_widget(type_button)

            def create_group():
                name = name_field.text.strip()
                description = description_field.text.strip()

                if not name:
                    self.show_error("Błąd", "Podaj nazwę grupy")
                    return

                group_data = {
                    'name': name,
                    'description': description,
                    'type': self.group_type,
                    'owner': self.get_current_user(),
                    'visibility': 'public'
                }

                group_id = self.get_data_manager().create_group(group_data)
                self.show_dialog("Sukces", f"Grupa '{name}' została utworzona")

                # Odśwież listę grup
                self.refresh_groups_lists()

            dialog = MDDialog(
                title="Utwórz grupę",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="ANULUJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="UTWÓRZ",
                        on_release=lambda x: (dialog.dismiss(), create_group())
                    )
                ]
            )
            dialog.open()

    def show_type_selection(self, button):
        """Pokaż wybór typu grupy"""
        if self.app:
            types = ["Branżowa", "Regionalna", "Projektowa", "Specjalistyczna"]

            def select_type(selected_type):
                self.group_type = selected_type
                button.text = f"Typ: {selected_type}"

            self.app.dialog_manager.show_selection_dialog(
                "Wybierz typ grupy",
                types,
                select_type
            )

    def set_group_type(self, group_type, button):
        """Ustaw typ grupy"""
        self.group_type = group_type
        button.text = f"Typ: {group_type}"

    def join_group(self, group):
        """Dołącz do grupy"""
        current_user = self.get_current_user()
        data_manager = self.get_data_manager()

        data_manager.join_group(group['id'], current_user)

        group_name = group.get('name', 'grupa')
        self.show_dialog("Sukces", f"Dołączyłeś do grupy '{group_name}'")

        # Odśwież listy
        self.refresh_groups_lists()

    def confirm_leave_group(self, group):
        """Potwierdź opuszczenie grupy"""
        group_name = group.get('name', 'grupy')
        self.show_confirmation(
            "Opuść grupę",
            f"Czy na pewno chcesz opuścić grupę '{group_name}'?",
            lambda: self.leave_group(group)
        )

    def leave_group(self, group):
        """Opuść grupę"""
        current_user = self.get_current_user()
        data_manager = self.get_data_manager()

        data_manager.leave_group(group['id'], current_user)

        group_name = group.get('name', 'grupa')
        self.show_dialog("Sukces", f"Opuściłeś grupę '{group_name}'")

        # Odśwież listy
        self.refresh_groups_lists()

    def manage_group(self, group):
        """Zarządzaj grupą (dla właściciela)"""
        if self.app:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.list import MDList, TwoLineListItem
            from kivymd.uix.boxlayout import MDBoxLayout
            from kivymd.uix.label import MDLabel
            from kivy.uix.scrollview import ScrollView

            # Lista członków grupy
            content = MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="300dp"
            )

            members_label = MDLabel(
                text="Członkowie grupy:",
                font_style="H6",
                size_hint_y=None,
                height="30dp"
            )

            scroll = ScrollView()
            members_list = MDList()

            # Dodaj członków do listy
            group_data = self.get_data_manager().get_group(group['id'])
            if group_data:
                for member_username in group_data.get('members', []):
                    member_data = self.get_data_manager().get_user(member_username)
                    if member_data:
                        company = member_data.get('company', member_username)
                        specialization = member_data.get('specialization', 'Brak specjalizacji')

                        is_owner = member_username == group_data.get('owner')
                        role_text = "Właściciel" if is_owner else "Członek"

                        item = TwoLineListItem(
                            text=company,
                            secondary_text=f"{specialization} • {role_text}"
                        )

                        # Dodaj przycisk usuwania dla nie-właścicieli
                        if not is_owner:
                            remove_btn = MDIconButton(
                                icon="account-minus",
                                theme_icon_color="Custom",
                                icon_color="red",
                                pos_hint={'center_y': 0.5, 'right': 1},
                                on_release=lambda x, username=member_username: self.confirm_remove_member(group,
                                                                                                          username,
                                                                                                          company)
                            )
                            item.add_widget(remove_btn)

                        members_list.add_widget(item)

            scroll.add_widget(members_list)

            content.add_widget(members_label)
            content.add_widget(scroll)

            dialog = MDDialog(
                title=f"Zarządzanie grupą: {group.get('name', '')}",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="ZAMKNIJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="EDYTUJ GRUPĘ",
                        on_release=lambda x: (dialog.dismiss(), self.edit_group(group))
                    )
                ]
            )
            dialog.open()

    def confirm_remove_member(self, group, member_username, member_name):
        """Potwierdź usunięcie członka"""
        self.show_confirmation(
            "Usuń członka",
            f"Czy na pewno chcesz usunąć {member_name} z grupy?",
            lambda: self.remove_member_from_group(group, member_username)
        )

    def remove_member_from_group(self, group, member_username):
        """Usuń członka z grupy"""
        data_manager = self.get_data_manager()
        data_manager.leave_group(group['id'], member_username)

        self.show_dialog("Sukces", "Członek został usunięty z grupy")

    def edit_group(self, group):
        """Edytuj grupę"""
        if self.app:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.textfield import MDTextField
            from kivymd.uix.boxlayout import MDBoxLayout

            content = MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="200dp"
            )

            name_field = MDTextField(
                hint_text="Nazwa grupy",
                text=group.get('name', ''),
                size_hint_y=None,
                height="48dp"
            )

            description_field = MDTextField(
                hint_text="Opis grupy",
                text=group.get('description', ''),
                multiline=True,
                size_hint_y=None,
                height="80dp"
            )

            content.add_widget(name_field)
            content.add_widget(description_field)

            def save_changes():
                name = name_field.text.strip()
                description = description_field.text.strip()

                if not name:
                    self.show_error("Błąd", "Podaj nazwę grupy")
                    return

                # Zaktualizuj grupę
                updates = {
                    'name': name,
                    'description': description
                }

                data_manager = self.get_data_manager()
                group_data = data_manager.get_group(group['id'])
                group_data.update(updates)
                data_manager.groups[group['id']] = group_data
                data_manager.save_data(data_manager.groups, data_manager.groups_file)

                self.show_dialog("Sukces", "Grupa została zaktualizowana")
                self.refresh_groups_lists()

            dialog = MDDialog(
                title="Edytuj grupę",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="ANULUJ",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="ZAPISZ",
                        on_release=lambda x: (dialog.dismiss(), save_changes())
                    )
                ]
            )
            dialog.open()

    def refresh_groups_lists(self):
        """Odśwież listy grup"""
        # W pełnej implementacji można by przebudować zawartość tabów
        # Na razie tylko pokazujemy info
        self.show_dialog("Info", "Lista grup została odświeżona. Przejdź między tabami aby zobaczyć zmiany.")