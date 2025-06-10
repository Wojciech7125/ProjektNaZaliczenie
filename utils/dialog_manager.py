from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem


class DialogManager:
    def __init__(self):
        self.current_dialog = None

    def show_info_dialog(self, title, text, callback=None):
        """Pokaż dialog informacyjny"""
        self.current_dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.close_dialog(callback)
                )
            ]
        )
        self.current_dialog.open()

    def show_error_dialog(self, title, text, callback=None):
        """Pokaż dialog błędu"""
        self.current_dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color="red",
                    on_release=lambda x: self.close_dialog(callback)
                )
            ]
        )
        self.current_dialog.open()

    def show_confirmation_dialog(self, title, text, on_confirm, on_cancel=None):
        """Pokaż dialog potwierdzenia"""
        self.current_dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="ANULUJ",
                    on_release=lambda x: self.close_dialog(on_cancel)
                ),
                MDRaisedButton(
                    text="POTWIERDŹ",
                    on_release=lambda x: self.close_dialog(on_confirm)
                )
            ]
        )
        self.current_dialog.open()

    def show_input_dialog(self, title, hint_text, on_confirm, on_cancel=None):
        """Pokaż dialog z polem tekstowym"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="120dp"
        )

        text_field = MDTextField(
            hint_text=hint_text,
            size_hint_y=None,
            height="48dp"
        )
        content.add_widget(text_field)

        self.current_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ANULUJ",
                    on_release=lambda x: self.close_dialog(on_cancel)
                ),
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.close_dialog(
                        lambda: on_confirm(text_field.text) if on_confirm else None
                    )
                )
            ]
        )
        self.current_dialog.open()

    def show_selection_dialog(self, title, items, on_select, on_cancel=None):
        """Pokaż dialog wyboru z listy"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="300dp"
        )

        items_list = MDList()

        for item in items:
            list_item = OneLineListItem(
                text=item,
                on_release=lambda x, selected_item=item: self.close_dialog(
                    lambda: on_select(selected_item) if on_select else None
                )
            )
            items_list.add_widget(list_item)

        content.add_widget(items_list)

        self.current_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ANULUJ",
                    on_release=lambda x: self.close_dialog(on_cancel)
                )
            ]
        )
        self.current_dialog.open()

    def show_loading_dialog(self, title="Ładowanie...", text="Proszę czekać"):
        """Pokaż dialog ładowania"""
        self.current_dialog = MDDialog(
            title=title,
            text=text,
            auto_dismiss=False
        )
        self.current_dialog.open()

    def close_dialog(self, callback=None):
        """Zamknij aktualny dialog"""
        if self.current_dialog:
            self.current_dialog.dismiss()
            self.current_dialog = None

        if callback:
            callback()

    def show_project_details_dialog(self, project, app):
        """Pokaż szczegóły projektu"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="400dp"
        )

        # Dodaj informacje o projekcie
        from kivymd.uix.label import MDLabel

        details_text = f"""
Nazwa: {project.get('name', 'Brak nazwy')}
Lokalizacja: {project.get('location', 'Brak lokalizacji')}
Powierzchnia: {project.get('area', 'Nie podano')}
Objętość: {project.get('volume', 'Nie podano')}
Budżet: {project.get('budget', 'Nie podano')}
Status: {project.get('status', 'Nieznany')}
Autor: {project.get('author', 'Nieznany')}

Opis:
{project.get('description', 'Brak opisu')}
        """.strip()

        details_label = MDLabel(
            text=details_text,
            theme_text_color="Primary",
            size_hint_y=None,
            text_size=(None, None),
            valign="top"
        )

        content.add_widget(details_label)

        buttons = [
            MDFlatButton(
                text="ZAMKNIJ",
                on_release=lambda x: self.close_dialog()
            )
        ]

        # Dodaj przyciski w zależności od roli użytkownika
        current_user = app.get_current_user()
        if project.get('author') == current_user:
            buttons.insert(0, MDRaisedButton(
                text="EDYTUJ",
                on_release=lambda x: self.close_dialog(
                    lambda: app.change_screen('new_project')  # TODO: przekaż ID projektu
                )
            ))
        else:
            buttons.insert(0, MDRaisedButton(
                text="ZŁÓŻ OFERTĘ",
                on_release=lambda x: self.close_dialog(
                    lambda: self.show_offer_dialog(project, app)
                )
            ))

        self.current_dialog = MDDialog(
            title="Szczegóły projektu",
            type="custom",
            content_cls=content,
            buttons=buttons
        )
        self.current_dialog.open()

    def show_offer_dialog(self, project, app):
        """Pokaż dialog składania oferty"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="200dp"
        )

        price_field = MDTextField(
            hint_text="Twoja cena (PLN)",
            input_filter="float",
            size_hint_y=None,
            height="48dp"
        )

        description_field = MDTextField(
            hint_text="Opis oferty",
            multiline=True,
            size_hint_y=None,
            height="80dp"
        )

        content.add_widget(price_field)
        content.add_widget(description_field)

        def submit_offer():
            if not price_field.text.strip():
                self.show_error_dialog("Błąd", "Podaj cenę oferty")
                return

            offer_data = {
                'author': app.get_current_user(),
                'price': price_field.text.strip(),
                'description': description_field.text.strip()
            }

            app.data_manager.add_offer_to_project(project['id'], offer_data)
            self.show_info_dialog("Sukces", "Oferta została wysłana")

        self.current_dialog = MDDialog(
            title="Złóż ofertę",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ANULUJ",
                    on_release=lambda x: self.close_dialog()
                ),
                MDRaisedButton(
                    text="WYŚLIJ OFERTĘ",
                    on_release=lambda x: self.close_dialog(submit_offer)
                )
            ]
        )
        self.current_dialog.open()