# ux/dashboard.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

class DashboardScreen(MDScreen):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.label = MDLabel(
            text="Welcome to Pentest System\nSelect a module from the navigation bar.",
            halign="center",
            theme_text_color="Primary"
        )
        self.add_widget(self.label)

    def update_language(self, lang: str):
        self.label.text = (
            "Welcome to Pentest System\nSelect a module from the navigation bar." if lang == 'en'
            else "Pentest Sistemine Hoş Geldiniz\nNavigasyon çubuğundan bir modül seçin."
        )

    def update_theme(self):
        pass  # Handled by KivyMD theme