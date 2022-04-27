import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar

from src.main import Portfolios

portfolios = Portfolios()
main_kv_file = "mainscreen.kv"

class MyScreenManager(ScreenManager):
    
    def change_screen(self, name):
        self.current = name

class MainScreen(Screen):
    pass

class PortfolioScreen(Screen):
    pass

class Main(MDApp):

    def build(self):
        self.load_kv(main_kv_file)
        self.sm = MyScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        return self.sm

    def call_method(self, klass_, method_):
        klass = getattr(sys.modules[__name__], klass_)
        x = klass()
        method = getattr(x, method_)
        method()

    def add_screen(self, name):
        self.sm.add_widget(PortfolioScreen(name=name))


class AddPortfolio(MDBoxLayout):
    name = ObjectProperty()
    pass


class MyDialog(MDDialog):

    def __init__(self):
        kwargs = {
            'content_cls': AddPortfolio(),
            'title': 'Add new portfolio',
            'type': 'custom',
            'buttons': [
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda _: self.dismiss()
                ),
                MDFlatButton(
                    text='Add',
                    on_release=lambda _: self.get_text()
                )
            ]
        }
        super().__init__(**kwargs)

    def get_text(self):
        textfield = self.content_cls.name
        name = textfield.text
        if name:
            print(self.content_cls.name.text)
            if name in portfolios.instances.keys():
                textfield.error=True
                textfield.helper_text="{} has already been created".format(name)
            else:
                portfolios.create_instance(name)
                MDApp.get_running_app().add_screen(name)
                self.dismiss()


if __name__ == "__main__":
    Main().run()
