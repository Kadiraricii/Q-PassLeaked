# ux/static/contact.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
import urllib.parse
import webbrowser


class ContactScreen(MDScreen):
    language = StringProperty('en')

    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.layout = MDBoxLayout(orientation='vertical', padding="10dp", spacing="10dp")

        self.name_input = MDTextField(hint_text="Your name" if self.language == 'en' else "Adınız")
        self.email_input = MDTextField(hint_text="Your email" if self.language == 'en' else "E-postanız")
        self.phone_input = MDTextField(
            hint_text="Your phone number (optional)" if self.language == 'en' else "Telefon numaranız (isteğe bağlı)")
        self.github_input = MDTextField(
            hint_text="Your GitHub username (optional)" if self.language == 'en' else "GitHub kullanıcı adınız (isteğe bağlı)")
        self.message_input = MDTextField(hint_text="Your message" if self.language == 'en' else "Mesajınız",
                                         multiline=True)
        self.send_button = MDRaisedButton(
            text="Send" if self.language == 'en' else "Gönder",
            pos_hint={"center_x": 0.5},
            on_release=self.send_email
        )

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.phone_input)
        self.layout.add_widget(self.github_input)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.send_button)
        self.add_widget(self.layout)

    def send_email(self, instance):
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        message = self.message_input.text.strip()

        if not name or not email or not message:
            error_message = 'Please fill in all required fields.' if self.language == 'en' else 'Lütfen tüm zorunlu alanları doldurun.'
            dialog = MDDialog(
                title='Error / Hata',
                text=error_message,
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return

        phone = self.phone_input.text.strip()
        github = self.github_input.text.strip()
        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nGitHub: {github}\nMessage: {message}"
        subject = "Contact from Q-Pentest"
        mailto = f"mailto:info@q-e.io?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto)

    def update_language(self, lang):
        self.language = lang
        if lang == 'en':
            self.name_input.hint_text = 'Your name'
            self.email_input.hint_text = 'Your email'
            self.phone_input.hint_text = 'Your phone number (optional)'
            self.github_input.hint_text = 'Your GitHub username (optional)'
            self.message_input.hint_text = 'Your message'
            self.send_button.text = 'Send'
        else:  # 'tr'
            self.name_input.hint_text = 'Adınız'
            self.email_input.hint_text = 'E-postanız'
            self.phone_input.hint_text = 'Telefon numaranız (isteğe bağlı)'
            self.github_input.hint_text = 'GitHub kullanıcı adınız (isteğe bağlı)'
            self.message_input.hint_text = 'Mesajınız'
            self.send_button.text = 'Gönder'

    def update_theme(self):
        pass  # Handled by KivyMD