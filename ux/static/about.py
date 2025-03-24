# ux/static/about.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.asyncimage import AsyncImage
from kivy.properties import StringProperty

class AboutScreen(Screen):
    language = StringProperty('en')  # Default to English

    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
        self.build_content()

    def build_content(self):
        """Rebuild the layout based on the current language."""
        self.layout.clear_widgets()
        content = self.get_content(self.language)

        # Badges (same for both languages)
        badge_layout = BoxLayout(orientation='horizontal', spacing=5)
        for badge in content['badges']:
            badge_layout.add_widget(AsyncImage(source=badge))
        self.layout.add_widget(badge_layout)

        # Title
        self.layout.add_widget(Label(text=content['title'], font_size=24, bold=True))

        # Description
        self.layout.add_widget(Label(text=content['description']))

        # What's the Buzz / Nası Bir Şey?
        self.layout.add_widget(Label(text=content['buzz_title'], font_size=20, bold=True))
        self.layout.add_widget(Label(text=content['buzz_content']))

        # Features Table
        self.layout.add_widget(Label(text=content['features_title'], font_size=20, bold=True))
        features_table = GridLayout(cols=3, size_hint_y=None, spacing=5, padding=5)
        for row in content['features']:
            for cell in row:
                features_table.add_widget(Label(text=cell))
        self.layout.add_widget(features_table)
        self.layout.add_widget(Label(text=content['features_extra']))

        # Jump In / Hemen Başla
        self.layout.add_widget(Label(text=content['jump_title'], font_size=20, bold=True))
        self.layout.add_widget(Label(text=content['jump_content']))

        # Contributors
        self.layout.add_widget(Label(text=content['contributors_title'], font_size=20, bold=True))
        contributors_label = Label(text=content['contributors'], markup=True)
        contributors_label.bind(on_ref_press=self.open_link)
        self.layout.add_widget(contributors_label)

        # Slogan
        self.layout.add_widget(Label(text=content['slogan_title'], font_size=20, bold=True))
        self.layout.add_widget(Label(text=content['slogan']))

        # License
        self.layout.add_widget(Label(text=content['license_title'], font_size=20, bold=True))
        self.layout.add_widget(Label(text=content['license']))

    def get_content(self, lang):
        """Return content dictionary based on language."""
        if lang == 'en':
            return {
                'badges': [
                    'https://img.shields.io/badge/Pentest-Beast-brightgreen',
                    'https://img.shields.io/badge/AI-Charged-blue',
                    'https://img.shields.io/badge/Speed-Lightning-red'
                ],
                'title': 'Q-Pentest',
                'description': 'Unleash the ultimate pentesting vibe! Crush weeks of work into hours with epic code. Future-proof your skills for 2025 tech—let’s rock it!',
                'buzz_title': 'What’s the Buzz?',
                'buzz_content': 'Hack everything:\n- Websites, WiFi, Bluetooth\n- Apps, routers, networks\n- MITM and beyond!\n\nNot just AI—our +15 years of algorithm mastery and prompt wizardry make it unstoppable.\nAlgorithms + Problem Solving + AI = PURE MAGIC.',
                'features_title': 'Features',
                'features': [
                    ['Target', 'Move', 'Weapon'],
                    ['Networks', 'Scan & Strike', 'nmap_module.py'],
                    ['Web', 'Inject & Grab', 'requests_module.py'],
                    ['WiFi/BT', 'Jam & Snag', 'wifi_module.py'],
                    ['Apps', 'Hook & Own', 'frida_module.py']
                ],
                'features_extra': '- Blazing Fast: Code drops like fire.\n- Everywhere: Windows, macOS, Linux.\n- Next-Level: Built for 2025.',
                'jump_title': 'Jump In',
                'jump_content': '1. Grab: git clone <repo>\n2. Gear Up: pip install -r requirements.txt\n3. Blast Off: python -m modules.<module_name>',
                'contributors_title': 'Contributors',
                'contributors': '[ref=https://github.com/keyvanarasteh]Keyvan Arasteh[/ref]\n[ref=https://github.com/mrrtzz]Morteza Azmude[/ref]\n\nYoung coders, join us—build the future!',
                'slogan_title': 'Slogan',
                'slogan': 'Machines Unleash Insane Speed!',
                'license_title': 'License',
                'license': 'This project is dual-licensed. See LICENSE.md for details:\n- Free for personal and educational use.\n- Commercial use requires a 5% donation of income above $10K to the developers.'
            }
        else:  # 'tr'
            return {
                'badges': [
                    'https://img.shields.io/badge/Pentest-Beast-brightgreen',
                    'https://img.shields.io/badge/AI-Charged-blue',
                    'https://img.shields.io/badge/Speed-Lightning-red'
                ],
                'title': 'Pentest Canavarı',
                'description': 'Sızma testinde çığır aç! Haftalık işleri saatlere indir, kodla destan yaz. 2025 teknolojilerine hazır ol—hadi coşalım!',
                'buzz_title': 'Nası Bir Şey?',
                'buzz_content': 'Her şeyi hackle:\n- Web, WiFi, Bluetooth\n- Uygulamalar, router’lar, ağlar\n- MITM ve daha fazlası!\n\nSadece AI değil—+15 yıllık algoritma ustalığımız ve prompt sihirbazlığımızla durdurulamazız.\nAlgoritma + Problem Çözme + AI = SAF BÜYÜ.',
                'features_title': 'Özellikler',
                'features': [
                    ['Hedef', 'Hamle', 'Silah'],
                    ['Ağlar', 'Tara & Vur', 'nmap_module.py'],
                    ['Web', 'Enjekte & Kap', 'requests_module.py'],
                    ['WiFi/BT', 'Boz & Çal', 'wifi_module.py'],
                    ['Uygulamalar', 'Bağla & Ele Geç', 'frida_module.py']
                ],
                'features_extra': '- Alev Hızlı: Kodlar şimşek gibi.\n- Her Yerde: Windows, macOS, Linux.\n- Yeni Nesil: 2025 için hazır.',
                'jump_title': 'Hemen Başla',
                'jump_content': '1. Al: git clone <repo>\n2. Hazır Ol: pip install -r requirements.txt\n3. Uçuşa Geç: python -m modules.<module_name>',
                'contributors_title': 'Katkıda Bulunanlar',
                'contributors': '[ref=https://github.com/keyvanarasteh]Keyvan Arasteh[/ref]\n[ref=https://github.com/mrrtzz]Morteza Azmude[/ref]\n\nGenç kodcular, bize katılın—geleceği inşa edelim!',
                'slogan_title': 'Slogan',
                'slogan': 'Makinelerle Çıldırmış Gibi Hızlan!',
                'license_title': 'Lisans',
                'license': 'Bu proje ikili lisanslıdır. Detaylar için LICENSE.md\'ye bakın:\n- Kişisel ve eğitim amaçlı kullanım ücretsiz.\n- Ticari kullanım, 10 bin dolar üzeri gelirde geliştiricilere %5 bağış gerektirir.'
            }

    def open_link(self, instance, value):
        """Open URLs when contributor links are clicked."""
        import webbrowser
        webbrowser.open(value)

    def update_language(self, lang):
        """Update the screen content when language changes."""
        self.language = lang
        self.build_content()