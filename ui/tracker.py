from cgitb import text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from src.main import Portfolios

Window.size = (360, 640)
main_kv_file = "mainscreen.kv"

class MyScreenManager(ScreenManager):
    
    def change_screen(self, name):
        self.current = name

class MainScreen(Screen):
    pass

class PortfolioScreen(Screen):
    currency = ObjectProperty()

class Main(MDApp):
    portfolios = Portfolios()
    sm = MyScreenManager()

    def build(self):
        self.load_kv(main_kv_file)
        self.sm.add_widget(MainScreen(name='main'))
        return self.sm

    def on_start(self):
        for name in self.portfolios.portfolio_names:
            currency = self.portfolios.instances[name].currency
            value = self.portfolios.instances[name].value
            self.add_screen(name, currency, value)

    def call_method(self, klass_, method_, **kwargs):
        klass = getattr(sys.modules[__name__], klass_)
        x = klass(**kwargs)
        method = getattr(x, method_)
        method()

    def add_screen(self, name, currency=portfolios.currency, value=0):
        if self.portfolios.instances[name].value:
            value = self.portfolios.instances[name].value
        self.sm.add_widget(PortfolioScreen(name=name, currency=currency))
        self.sm.get_screen('main').ids['p_list'].add_widget(PortfolioButton(text=name, currency=currency, value=value))


class PortfolioButton(ButtonBehavior, MDBoxLayout):
    
    def __init__(self, text, currency=Main().portfolios.currency, value=0, **kwargs):
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
            'title': 'New transaction',
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
            if name in Main().portfolios.instances.keys():
                p_name.error=True
                p_name.helper_text="{} has already been created".format(name)
            else:
                Main().portfolios.create_instance(name, currency=curr)
                MDApp.get_running_app().add_screen(name, currency=curr)
                self.dismiss()


class NewTransaction(MDGridLayout):
    date = ObjectProperty()
    currency = ObjectProperty()
    type = ObjectProperty()
    amount = ObjectProperty()

class TransactionDialog(MDDialog):
    # portfolio_name = None

    def __init__(self, name):
        self.portfolio_name = name
        kwargs = {
            'content_cls': NewTransaction(),
            'title': 'New Transaction',
            'type': 'custom',
            'buttons': [
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda _: self.dismiss()
                ),
                MDFlatButton(
                    text='Add',
                    on_release=lambda _: self.new_transaction()
                )
            ]
        }
        super().__init__(**kwargs)

    def new_transaction(self):
        date = self.content_cls.date.text
        curr = self.content_cls.currency.text
        type = self.content_cls.type.text
        amount = int(self.content_cls.amount.text)
        transaction = {'date': date, 'currency': curr, 'type': type, 'amount': amount}
        if not curr:
            curr = Portfolios().currency
        Main().portfolios.instances[self.portfolio_name].cash.handle_transaction(transaction)
        self.dismiss()



if __name__ == "__main__":
    Main().run()
