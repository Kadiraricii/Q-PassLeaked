# ux/parent.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from ux.nav import NavigationBar


class ParentUX(BoxLayout):
    language = StringProperty('en')
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ParentUX, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.nav_bar = NavigationBar()
        self.add_widget(self.nav_bar)

        self.screen_manager = ScreenManager()
        self.add_widget(self.screen_manager)
        # Placeholder for adding screens later

    def change_language(self, lang: str):
        """Change the application language."""
        self.language = lang
        self.nav_bar.update_language(lang)
        for screen in self.screen_manager.screens:
            screen.update_language(lang)


class PentestApp(App):
    def build(self):
        return ParentUX()


if __name__ == '__main__':
    PentestApp().run()