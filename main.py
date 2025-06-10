from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.main_screen import MainScreen
from screens.projects_screen import ProjectsScreen
from screens.new_project_screen import NewProjectScreen
from screens.friends_screen import FriendsScreen
from screens.groups_screen import GroupsScreen
from screens.profile_screen import ProfileScreen
from utils.data_manager import DataManager
from utils.dialog_manager import DialogManager


class ZleceniaApp(MDApp):
    def __init__(self):
        super().__init__()
        self.title = "Zlecenia Pro"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "DeepOrange"

        # Inicjalizuj managery
        self.data_manager = DataManager()
        self.dialog_manager = DialogManager()

        # Stan aplikacji
        self.current_user = None

    def build(self):
        self.sm = MDScreenManager()

        # Dodaj wszystkie ekrany
        self.sm.add_widget(LoginScreen(name='login', app=self))
        self.sm.add_widget(RegisterScreen(name='register', app=self))
        self.sm.add_widget(MainScreen(name='main', app=self))
        self.sm.add_widget(ProjectsScreen(name='projects', app=self))
        self.sm.add_widget(NewProjectScreen(name='new_project', app=self))
        self.sm.add_widget(FriendsScreen(name='friends', app=self))
        self.sm.add_widget(GroupsScreen(name='groups', app=self))
        self.sm.add_widget(ProfileScreen(name='profile', app=self))

        return self.sm

    def change_screen(self, screen_name):
        """Zmień ekran"""
        self.sm.current = screen_name

    def set_current_user(self, username):
        """Ustaw aktualnego użytkownika"""
        self.current_user = username

    def get_current_user(self):
        """Pobierz aktualnego użytkownika"""
        return self.current_user

    def logout(self):
        """Wyloguj użytkownika"""
        self.current_user = None
        self.change_screen('login')


if __name__ == '__main__':
    ZleceniaApp().run()