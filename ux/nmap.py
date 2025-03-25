# ux/nmap.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from modules.nmap import NmapScanner
import json

class NmapScreen(MDScreen):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.scanner = NmapScanner()
        self.language = 'en'

        self.layout = MDBoxLayout(orientation='vertical', padding="10dp", spacing="10dp")
        self.hosts_input = MDTextField(hint_text="Hosts (e.g., 192.168.1.0/24)")
        self.ports_input = MDTextField(hint_text="Ports (e.g., 22-443)")
        self.args_input = MDTextField(hint_text="Arguments (e.g., -sS)")
        self.scan_button = MDRaisedButton(
            text="Scan" if self.language == 'en' else "Tarama",
            pos_hint={"center_x": 0.5},
            on_release=self.run_scan
        )
        self.result_scroll = MDScrollView()
        self.result_label = MDLabel(
            text="Scan results will appear here",
            halign="left",
            theme_text_color="Primary",
            size_hint_y=None,
            height="100dp"
        )
        self.result_scroll.add_widget(self.result_label)
        self.tutorial_button = MDRaisedButton(
            text="Show Tutorial" if self.language == 'en' else "Eğitimi Göster",
            pos_hint={"center_x": 0.5},
            on_release=self.show_tutorial
        )

        self.layout.add_widget(self.hosts_input)
        self.layout.add_widget(self.ports_input)
        self.layout.add_widget(self.args_input)
        self.layout.add_widget(self.scan_button)
        self.layout.add_widget(self.result_scroll)
        self.layout.add_widget(self.tutorial_button)
        self.add_widget(self.layout)

    def run_scan(self, instance):
        result = self.scanner.scan_network(
            hosts=self.hosts_input.text,
            ports=self.ports_input.text or None,
            arguments=self.args_input.text
        )
        self.result_label.text = str(result)
        self.result_label.height = self.result_label.texture_size[1]

    def show_tutorial(self, instance):
        try:
            with open(f'modules/nmap.{self.language}.json', 'r') as f:
                data = json.load(f)
            examples = data['functions']['scan_network']['description'].split('### Examples')[1]
            self.result_label.text = examples
            self.result_label.height = self.result_label.texture_size[1]
        except (FileNotFoundError, KeyError):
            self.result_label.text = "Tutorial not available."

    def update_language(self, lang: str):
        self.language = lang
        self.scan_button.text = 'Scan' if lang == 'en' else 'Tarama'
        self.tutorial_button.text = 'Show Tutorial' if lang == 'en' else 'Eğitimi Göster'
        self.hosts_input.hint_text = "Hosts (e.g., 192.168.1.0/24)"
        self.ports_input.hint_text = "Ports (e.g., 22-443)"
        self.args_input.hint_text = "Arguments (e.g., -sS)"

    def update_theme(self):
        pass  # Handled by KivyMD