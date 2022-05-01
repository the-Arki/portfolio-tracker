from cgitb import text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.properties import ObjectProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

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

    def on_start(self):
        for name in portfolios.portfolio_names:
            currency = portfolios.instances[name].currency
            value = portfolios.instances[name].value
            self.add_screen(name, currency, value)

    def call_method(self, klass_, method_):
        klass = getattr(sys.modules[__name__], klass_)
        x = klass()
        method = getattr(x, method_)
        method()

    def add_screen(self, name, currency=portfolios.currency, value=0):
        if portfolios.instances[name].value:
            value = portfolios.instances[name].value
        self.sm.add_widget(PortfolioScreen(name=name))
        self.sm.get_screen('main').ids['p_list'].add_widget(PortfolioButton(text=name, currency=currency, value=value))


class PortfolioButton(ButtonBehavior, MDBoxLayout):
    
    def __init__(self, text, currency=portfolios.currency, value=0, **kwargs):
        self.text = text
        self.currency = currency
        self.value = value

        super().__init__(**kwargs)


class AddPortfolio(MDBoxLayout):
    name = ObjectProperty()
    currency = ObjectProperty()


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
                    on_release=lambda _: self.add_portfolio()
                )
            ]
        }
        super().__init__(**kwargs)

    def add_portfolio(self):
        p_name = self.content_cls.name
        name = p_name.text
        curr = self.content_cls.currency.text
        if not curr:
            curr = Portfolios().currency

        if name:
            if name in portfolios.instances.keys():
                p_name.error=True
                p_name.helper_text="{} has already been created".format(name)
            else:
                portfolios.create_instance(name, currency=curr)
                MDApp.get_running_app().add_screen(name, currency=curr)
                self.dismiss()


if __name__ == "__main__":
    Main().run()
