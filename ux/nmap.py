from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from modules.nmap import NmapScanner
import json


class NmapScreen(Screen):
    def __init__(self, **kwargs):
        super(NmapScreen, self).__init__(**kwargs)
        self.scanner = NmapScanner()
        self.language = 'en'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.hosts_input = TextInput(hint_text='Hosts (e.g., 192.168.1.0/24)')
        self.ports_input = TextInput(hint_text='Ports (e.g., 22-443)')
        self.args_input = TextInput(hint_text='Arguments (e.g., -sS)')
        self.scan_button = Button(text='Scan', on_press=self.run_scan)
        self.result_label = Label(text='Scan results will appear here')
        self.tutorial_button = Button(text='Show Tutorial', on_press=self.show_tutorial)

        layout.add_widget(self.hosts_input)
        layout.add_widget(self.ports_input)
        layout.add_widget(self.args_input)
        layout.add_widget(self.scan_button)
        layout.add_widget(self.result_label)
        layout.add_widget(self.tutorial_button)
        self.add_widget(layout)

    def run_scan(self, instance):
        result = self.scanner.scan_network(
            hosts=self.hosts_input.text,
            ports=self.ports_input.text or None,
            arguments=self.args_input.text
        )
        self.result_label.text = str(result)

    def show_tutorial(self, instance):
        with open(f'modules/nmap.{self.language}.json', 'r') as f:
            data = json.load(f)
        examples = data['functions']['scan_network']['description'].split('### Examples')[1]
        self.result_label.text = examples

    def update_language(self, lang: str):
        self.language = lang
        self.scan_button.text = 'Scan' if lang == 'en' else 'Tarama'
        self.tutorial_button.text = 'Show Tutorial' if lang == 'en' else 'Eğitimi Göster'