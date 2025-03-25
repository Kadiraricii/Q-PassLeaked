# ux/nav.py
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.properties import StringProperty, ObjectProperty

class NavigationDrawer(MDNavigationDrawer):
    language = StringProperty('en')
    theme = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = "200dp"
        self.list_view = MDList()
        self.add_widget(self.list_view)
        self.rebuild_drawer()

    def add_category(self, category_name, items):
        for item in items:
            btn = OneLineIconListItem(
                text=item if self.language == 'en' else self.translate_item(item),
                on_release=lambda x, screen=item.lower(): self.go_to_screen(screen)
            )
            btn.add_widget(IconLeftWidget(icon=self.get_icon(item)))
            self.list_view.add_widget(btn)

    def go_to_screen(self, screen_name):
        self.parent.manager.current = screen_name
        self.set_state("close")

    def get_icon(self, item):
        icons = {
            'Dashboard': 'view-dashboard',
            'Nmap': 'network',
            'About': 'information',
            'Contact': 'email'
        }
        return icons.get(item, 'circle')

    def translate_item(self, item):
        translations = {
            'Dashboard': 'Pano',
            'Nmap': 'Nmap',
            'About': 'Hakkında',
            'Contact': 'İletişim'
        }
        return translations.get(item, item)

    def update_language(self, lang: str):
        self.language = lang
        self.rebuild_drawer()

    def update_theme(self):
        pass  # Theme handled by KivyMD

    def rebuild_drawer(self):
        self.list_view.clear_widgets()
        self.add_category('General', ['Dashboard', 'Contact'])
        self.add_category('Network', ['Nmap'])
        self.add_category('Static', ['About'])