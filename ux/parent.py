# ux/parent.py
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationlayout import MDNavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty
from ux.nav import NavigationDrawer
from ux.routes import register_routes
from ux.theme import Theme

class ParentUX(MDBoxLayout):
    language = StringProperty('en')
    theme = ObjectProperty(None)
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical')
        self.theme = Theme()
        self.toolbar = MDTopAppBar(title="Q-Pentest")
        self.toolbar.left_action_items = [["menu", lambda x: self.toggle_drawer()]]
        self.toolbar.right_action_items = [["cog", lambda x: self.show_settings()]]

        self.screen_manager = MDScreenManager()
        self.nav_drawer = NavigationDrawer(theme=self.theme)
        navigation_layout = MDNavigationLayout()
        navigation_layout.add_widget(self.screen_manager)
        navigation_layout.add_widget(self.nav_drawer)

        self.add_widget(self.toolbar)
        self.add_widget(navigation_layout)

        register_routes(self.screen_manager, self.theme)
        self.screen_manager.current = 'dashboard'
        self.screen_manager.bind(current=self.update_app_bar)

    def toggle_drawer(self):
        self.nav_drawer.set_state("close" if self.nav_drawer.state == "open" else "open")

    def update_app_bar(self, instance, value):
        if value == "dashboard":
            self.toolbar.left_action_items = [["menu", lambda x: self.toggle_drawer()]]
            self.toolbar.title = "Dashboard"
        else:
            self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
            self.toolbar.title = value.capitalize()

    def go_back(self):
        self.screen_manager.current = "dashboard"

    def show_settings(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        content = MDBoxLayout(orientation="vertical", padding="10dp", spacing="10dp")
        lang_en = MDFlatButton(text="English", on_release=lambda x: self.change_language('en'))
        lang_tr = MDFlatButton(text="Türkçe", on_release=lambda x: self.change_language('tr'))
        theme_light = MDFlatButton(text="Light Mode", on_release=lambda x: self.change_theme('light'))
        theme_dark = MDFlatButton(text="Dark Mode", on_release=lambda x: self.change_theme('dark'))
        theme_auto = MDFlatButton(text="Auto Mode", on_release=lambda x: self.change_theme('auto'))
        content.add_widget(lang_en)
        content.add_widget(lang_tr)
        content.add_widget(theme_light)
        content.add_widget(theme_dark)
        content.add_widget(theme_auto)
        dialog = MDDialog(title="Settings", type="custom", content_cls=content)
        dialog.open()

    def change_language(self, lang: str):
        self.language = lang
        self.nav_drawer.update_language(lang)
        for screen in self.screen_manager.screens:
            screen.update_language(lang)

    def change_theme(self, mode: str):
        self.theme.set_mode(mode)
        for screen in self.screen_manager.screens:
            screen.update_theme()

class PentestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return ParentUX()