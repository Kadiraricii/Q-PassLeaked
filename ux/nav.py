# ux/nav.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

class NavigationBar(BoxLayout):
    language = StringProperty('en')

    def __init__(self, **kwargs):
        super(NavigationBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.add_widget(Button(text='Dashboard', on_press=self.go_to_dashboard))
        self.add_widget(Button(text='Nmap', on_press=self.go_to_nmap))

    def go_to_dashboard(self, instance):
        self.parent.screen_manager.current = 'dashboard'

    def go_to_nmap(self, instance):
        self.parent.screen_manager.current = 'nmap'

    def update_language(self, lang: str):
        self.language = lang
        # Update button texts based on language (to be expanded)