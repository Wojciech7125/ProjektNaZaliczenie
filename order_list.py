from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.widget import Widget


class OrderListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing='10dp'
        )

        # Toolbar z przyciskiem menu
        toolbar = MDTopAppBar(
            title="",
            md_bg_color=(0.149, 0.267, 0.298, 1),
            left_action_items=[["menu", lambda x: None]],
            elevation=0
        )

        # Layout dla pola wyszukiwania i filtrów
        search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing='10dp',
            size_hint_y=None,
            height='60dp',
            padding=['10dp', '10dp']
        )

        # Pole wyszukiwania
        search_field = MDTextField(
            hint_text="Szukaj...",
            size_hint_x=0.7,
            mode="round",
            line_color_focus=(1, 0.5, 0, 1),
            line_color_normal=(1, 0.5, 0, 1)
        )

        # Przycisk filtrów
        filter_button = MDRaisedButton(
            text="Filtry",
            size_hint_x=0.3,
            md_bg_color=(1, 0.5, 0, 1)
        )

        search_layout.add_widget(search_field)
        search_layout.add_widget(filter_button)

        # ScrollView dla listy zamówień
        scroll = MDScrollView()
        orders_layout = MDBoxLayout(
            orientation='vertical',
            spacing='10dp',
            adaptive_height=True,
            padding='10dp'
        )

        # Przykładowe zamówienia
        for i in range(5):
            order_card = self.create_order_card(f"Nazwa Projektu {i + 1}", "użytkownik")
            orders_layout.add_widget(order_card)

        # Przycisk "Dodaj Zlecenie"
        add_order_button = MDRaisedButton(
            text="Dodaj Zlecenie",
            size_hint_y=None,
            height='50dp',
            md_bg_color=(1, 0.5, 0, 1),
            pos_hint={'center_x': 0.5},
            on_release=self.add_order
        )
        orders_layout.add_widget(add_order_button)

        scroll.add_widget(orders_layout)

        # Dolny pasek nawigacji
        bottom_nav = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='80dp',
            md_bg_color=(0.149, 0.267, 0.298, 1),
            spacing='20dp',
            padding='20dp'
        )

        # Przyciski dolnego paska
        received_button = MDRaisedButton(
            text="Odebrane",
            size_hint_x=0.5,
            md_bg_color=(1, 0.5, 0, 1)
        )

        sent_button = MDTextButton(
            text="Wysłane",
            size_hint_x=0.5,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )

        bottom_nav.add_widget(received_button)
        bottom_nav.add_widget(sent_button)

        main_layout.add_widget(toolbar)
        main_layout.add_widget(search_layout)
        main_layout.add_widget(scroll)
        main_layout.add_widget(bottom_nav)

        self.add_widget(main_layout)

    def create_order_card(self, project_name, user):
        card = MDCard(
            size_hint_y=None,
            height='120dp',
            elevation=2,
            md_bg_color=(0.149, 0.267, 0.298, 1),
            radius=[10],
            padding='15dp',
            on_release=self.open_order_details
        )

        card_layout = MDBoxLayout(
            orientation='horizontal',
            spacing='15dp'
        )

        # Ikona użytkownika
        user_icon = MDLabel(
            text="A",
            size_hint_x=None,
            width='40dp',
            font_size='24sp',
            theme_text_color="Custom",
            text_color=(1, 0.5, 0, 1),
            halign="center",
            valign="center"
        )

        # Informacje o projekcie
        project_info = MDBoxLayout(
            orientation='vertical',
            spacing='5dp'
        )

        project_title = MDLabel(
            text=project_name,
            font_size='16sp',
            theme_text_color="Primary",
            size_hint_y=None,
            height='30dp',
            bold=True
        )

        project_user = MDLabel(
            text=user,
            font_size='12sp',
            theme_text_color="Secondary",
            size_hint_y=None,
            height='20dp'
        )

        project_details = MDBoxLayout(
            orientation='vertical',
            spacing='2dp'
        )

        for detail in ["Miejsce", "Powierzchnia", "Prace"]:
            detail_label = MDLabel(
                text=detail,
                font_size='12sp',
                theme_text_color="Secondary",
                size_hint_y=None,
                height='15dp'
            )
            project_details.add_widget(detail_label)

        project_info.add_widget(project_title)
        project_info.add_widget(project_user)
        project_info.add_widget(project_details)

        # Logo placeholder na prawej stronie
        logo_layout = MDBoxLayout(
            orientation='horizontal',
            spacing='5dp',
            size_hint_x=None,
            width='80dp',
            pos_hint={'center_y': 0.5}
        )

        triangle = MDLabel(
            text="▲",
            font_size='20sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        square = MDLabel(
            text="■",
            font_size='20sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        circle = MDLabel(
            text="●",
            font_size='20sp',
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )

        logo_layout.add_widget(triangle)
        logo_layout.add_widget(square)
        logo_layout.add_widget(circle)

        card_layout.add_widget(user_icon)
        card_layout.add_widget(project_info)
        card_layout.add_widget(logo_layout)

        card.add_widget(card_layout)
        return card

    def open_order_details(self, *args):
        self.manager.current = 'order_details'

    def add_order(self, *args):
        self.manager.current = 'order_form'