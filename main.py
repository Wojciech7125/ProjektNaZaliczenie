from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivy.core.window import Window

from login import LoginScreen
from register import RegisterScreen
from order_list import OrderListScreen
#from order_details import OrderDetailsScreen
#from order_form import OrderFormScreen


class MainApp(MDApp):
    def build(self):
        # Ustawienie koloru tła
        Window.clearcolor = (0.149, 0.267, 0.298, 1)  # Ciemny zielony/niebieski

        # Ustawienie tematu
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "Orange"

        # Utworzenie managera ekranów
        sm = MDScreenManager()

        # Dodanie ekranów
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(OrderListScreen(name='order_list'))
        #sm.add_widget(OrderDetailsScreen(name='order_details'))
        #sm.add_widget(OrderFormScreen(name='order_form'))

        return sm


if __name__ == '__main__':
    MainApp().run()