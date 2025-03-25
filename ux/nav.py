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
        self.add_widget(Button(text='About', on_press=self.go_to_about))
        self.add_widget(Button(text='Contact', on_press=self.go_to_contact))

    def go_to_dashboard(self, instance):
        self.parent.screen_manager.current = 'dashboard'

    def go_to_nmap(self, instance):
        self.parent.screen_manager.current = 'nmap'

    def go_to_about(self, instance):
        self.parent.screen_manager.current = 'about'

    def go_to_contact(self, instance):
        self.parent.screen_manager.current = 'contact'

    def update_language(self, lang: str):
        self.language = lang
        if lang == 'en':
            self.children[3].text = 'Dashboard'
            self.children[2].text = 'Nmap'
            self.children[1].text = 'About'
            self.children[0].text = 'Contact'
        else:  # 'tr'
            self.children[3].text = 'Pano'
            self.children[2].text = 'Nmap'
            self.children[1].text = 'Hakkında'
            self.children[0].text = 'İletişim'