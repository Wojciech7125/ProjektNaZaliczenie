from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.metrics import dp


class ThemeHelper:
    """Helper class for consistent theming across the app"""

    COLORS = {
        'primary': '#ff7f00',  # Pomarańczowy - główny kolor
        'secondary': '#064653',  # Ciemny niebieskozielony - drugorzędny
        'background': '#022831',  # Najciemniejszy - tło
        'surface': '#064653',  # Powierzchnie kart
        'on_primary': '#ffffff',  # Tekst na głównym kolorze
        'on_surface': '#ffffff'  # Tekst na powierzchniach
    }

    @staticmethod
    def create_themed_card(height=None, **kwargs):
        """Utwórz kartę z motywem aplikacji"""
        default_props = {
            'md_bg_color': ThemeHelper.COLORS['surface'],
            'elevation': 0,  # Całkowicie wyłączone cienie
            'radius': [8],
            'padding': dp(15)
        }

        if height:
            default_props['height'] = height
            default_props['size_hint_y'] = None

        # Połącz z custom kwargs
        default_props.update(kwargs)

        return MDCard(**default_props)

    @staticmethod
    def create_primary_button(text, **kwargs):
        """Utwórz główny przycisk"""
        default_props = {
            'text': text,
            'md_bg_color': ThemeHelper.COLORS['primary'],
            'theme_text_color': 'Custom',
            'text_color': ThemeHelper.COLORS['on_primary'],
            'size_hint_y': None,
            'height': dp(48),
            'elevation': 0  # Wyłącz cienie
        }

        default_props.update(kwargs)
        return MDRaisedButton(**default_props)

    @staticmethod
    def create_secondary_button(text, **kwargs):
        """Utwórz drugorzędny przycisk"""
        default_props = {
            'text': text,
            'md_bg_color': ThemeHelper.COLORS['secondary'],
            'theme_text_color': 'Custom',
            'text_color': ThemeHelper.COLORS['on_surface'],
            'size_hint_y': None,
            'height': dp(48),
            'elevation': 0  # Wyłącz cienie
        }

        default_props.update(kwargs)
        return MDRaisedButton(**default_props)

    @staticmethod
    def create_flat_button(text, **kwargs):
        """Utwórz płaski przycisk"""
        default_props = {
            'text': text,
            'theme_text_color': 'Custom',
            'text_color': ThemeHelper.COLORS['primary'],
            'size_hint_y': None,
            'height': dp(36)
        }

        default_props.update(kwargs)
        return MDFlatButton(**default_props)
