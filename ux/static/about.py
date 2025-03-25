# ux/static/about.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
import webbrowser

class AboutScreen(MDScreen):
    language = StringProperty('en BANK')

    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.scroll_view = MDScrollView()
        self.layout = MDBoxLayout(orientation='vertical', padding="10dp", spacing="10dp", adaptive_height=True)
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)
        self.build_content()

    def build_content(self):
        self.layout.clear_widgets()
        content = self.get_content(self.language)

        for key, value in content.items():
            if key == 'badges':
                badge_layout = MDBoxLayout(orientation='horizontal', spacing="5dp", adaptive_height=True)
                for badge in value:
                    badge_layout.add_widget(MDLabel(text=badge, halign="center"))  # Placeholder; use images if PNGs available
                self.layout.add_widget(badge_layout)
            elif key in ['features']:
                feature_layout = MDBoxLayout(orientation='vertical', adaptive_height=True)
                for row in value:
                    row_layout = MDBoxLayout(orientation='horizontal', spacing="5dp", adaptive_height=True)
                    for cell in row:
                        row_layout.add_widget(MDLabel(text=cell, theme_text_color="Primary"))
                    feature_layout.add_widget(row_layout)
                self.layout.add_widget(feature_layout)
            elif key == 'contributors':
                label = MDLabel(text=value, markup=True, theme_text_color="Primary")
                label.bind(on_ref_press=self.open_link)
                self.layout.add_widget(label)
            else:
                self.layout.add_widget(MDLabel(
                    text=value,
                    theme_text_color="Primary",
                    halign="left" if 'title' not in key else "center",
                    font_style="H6" if 'title' in key else "Body1"
                ))

    def update_language(self, lang):
        self.language = lang
        self.build_content()

    def update_theme(self):
        pass  # Handled by KivyMD

    def open_link(self, instance, value):
        webbrowser.open(value)

    def get_content(self, lang):
        if lang == 'en':
            return {
                'badges': ['Pentest-Beast', 'AI-Charged', 'Speed-Lightning'],
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
        elif lang == 'tr':
            return {
                'badges': ['Pentest-Beast', 'AI-Charged', 'Speed-Lightning'],
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
        else:
            return self.get_content('en')  # Default to English