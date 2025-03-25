# ux/theme.py
from kivymd.theming import ThemableBehavior
from kivy.properties import StringProperty, DictProperty
from kivy.clock import Clock
import datetime

class Theme(ThemableBehavior):
    mode = StringProperty('light')  # 'light', 'dark', 'auto'
    colors = DictProperty()
    font_name = StringProperty('Roboto')  # Default font

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_colors()
        Clock.schedule_interval(self.check_auto_mode, 60)  # Check every minute

    def update_colors(self):
        if self.mode == 'dark' or (self.mode == 'auto' and self.is_night_time()):
            self.theme_cls.theme_style = "Dark"
            self.colors = {
                'background': '#1E1E1E',
                'foreground': '#D4D4D4',
                'accent': '#264F78',
                'secondary_bg': '#252526',
                'button_bg': '#333333',
                'button_text': '#D4D4D4'
            }
        else:
            self.theme_cls.theme_style = "Light"
            self.colors = {
                'background': '#FFFFFF',
                'foreground': '#000000',
                'accent': '#ADD6FF',
                'secondary_bg': '#F3F3F3',
                'button_bg': '#F8F8F8',
                'button_text': '#000000'
            }

    def is_night_time(self):
        now = datetime.datetime.now().time()
        return now >= datetime.time(18, 0) or now < datetime.time(6, 0)  # 6 PM to 6 AM

    def check_auto_mode(self, dt):
        if self.mode == 'auto':
            self.update_colors()

    def set_mode(self, mode):
        self.mode = mode
        self.update_colors()