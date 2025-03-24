from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Welcome to Pentest System\nSelect a module from the navigation bar.'))
        self.add_widget(layout)

    def update_language(self, lang: str):
        self.children[0].children[0].text = (
            'Welcome to Pentest System\nSelect a module from the navigation bar.' if lang == 'en'
            else 'Pentest Sistemine Hoş Geldiniz\nNavigasyon çubuğundan bir modül seçin.'
        )