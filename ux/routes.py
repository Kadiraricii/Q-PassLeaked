# ux/routes.py
from kivymd.uix.screenmanager import MDScreenManager
from ux.dashboard import DashboardScreen
from ux.nmap import NmapScreen
from ux.static.about import AboutScreen
from ux.static.contact import ContactScreen

def register_routes(screen_manager: MDScreenManager, theme):
    screen_manager.add_widget(DashboardScreen(theme=theme, name='dashboard'))
    screen_manager.add_widget(NmapScreen(theme=theme, name='nmap'))
    screen_manager.add_widget(AboutScreen(theme=theme, name='about'))
    screen_manager.add_widget(ContactScreen(theme=theme, name='contact'))