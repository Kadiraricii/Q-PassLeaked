from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import urllib.parse
import webbrowser

class ContactScreen(Screen):
    language = StringProperty('en')  # Default to English

    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Form fields
        self.name_label = Label(text='Name')
        self.name_input = TextInput(hint_text='Your name')
        self.email_label = Label(text='Email')
        self.email_input = TextInput(hint_text='Your email')
        self.phone_label = Label(text='Phone (optional)')
        self.phone_input = TextInput(hint_text='Your phone number')
        self.github_label = Label(text='GitHub username (optional)')
        self.github_input = TextInput(hint_text='Your GitHub username')
        self.message_label = Label(text='Message')
        self.message_input = TextInput(hint_text='Your message', multiline=True)
        self.send_button = Button(text='Send')
        self.send_button.bind(on_press=self.send_email)

        # Add widgets to layout
        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.email_label)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.phone_label)
        self.layout.add_widget(self.phone_input)
        self.layout.add_widget(self.github_label)
        self.layout.add_widget(self.github_input)
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.send_button)

        self.add_widget(self.layout)

    def send_email(self, instance):
        """Validate form and open email client with pre-filled email."""
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        message = self.message_input.text.strip()

        # Validate required fields
        if not name or not email or not message:
            error_message = 'Please fill in all required fields.' if self.language == 'en' else 'Lütfen tüm zorunlu alanları doldurun.'
            popup = Popup(title='Error / Hata', content=Label(text=error_message), size_hint=(0.5, 0.5))
            popup.open()
            return

        # Optional fields
        phone = self.phone_input.text.strip()
        github = self.github_input.text.strip()

        # Construct email body
        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nGitHub: {github}\nMessage: {message}"
        subject = "Contact from Q-Pentest"
        mailto = f"mailto:info@q-e.io?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto)

    def update_language(self, lang):
        """Update form labels and button text based on language."""
        self.language = lang
        if lang == 'en':
            self.name_label.text = 'Name'
            self.email_label.text = 'Email'
            self.phone_label.text = 'Phone (optional)'
            self.github_label.text = 'GitHub username (optional)'
            self.message_label.text = 'Message'
            self.send_button.text = 'Send'
            self.name_input.hint_text = 'Your name'
            self.email_input.hint_text = 'Your email'
            self.phone_input.hint_text = 'Your phone number'
            self.github_input.hint_text = 'Your GitHub username'
            self.message_input.hint_text = 'Your message'
        else:  # 'tr'
            self.name_label.text = 'İsim'
            self.email_label.text = 'E-posta'
            self.phone_label.text = 'Telefon (isteğe bağlı)'
            self.github_label.text = 'GitHub kullanıcı adı (isteğe bağlı)'
            self.message_label.text = 'Mesaj'
            self.send_button.text = 'Gönder'
            self.name_input.hint_text = 'Adınız'
            self.email_input.hint_text = 'E-postanız'
            self.phone_input.hint_text = 'Telefon numaranız'
            self.github_input.hint_text = 'GitHub kullanıcı adınız'
            self.message_input.hint_text = 'Mesajınız'