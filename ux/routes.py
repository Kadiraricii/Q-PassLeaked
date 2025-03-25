# ux/routes.py
from kivy.uix.screenmanager import ScreenManager
from ux.dashboard import DashboardScreen
from ux.nmap import NmapScreen
from ux.static.about import AboutScreen
from ux.static.contact import ContactScreen

def register_routes(screen_manager: ScreenManager):
    """Register all screens with the ScreenManager."""
    screen_manager.add_widget(DashboardScreen(name='dashboard'))
    screen_manager.add_widget(NmapScreen(name='nmap'))
    screen_manager.add_widget(AboutScreen(name='about'))
    screen_manager.add_widget(ContactScreen(name='contact'))