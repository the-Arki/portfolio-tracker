from locale import currency
import sys
import os

from numpy import kaiser
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
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


class Main(MDApp):
    portfolios = Portfolios()
    sm = MyScreenManager()
    portfolio_buttons = {}

    def build(self):
        self.load_kv(main_kv_file)
        value = int(self.portfolios.value)
        currency = self.portfolios.currency
        self.sm.add_widget(MainScreen(name='main', value=value, currency=currency))
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
        p_button = PortfolioButton(text=name, currency=currency, value=value)
        self.sm.add_widget(PortfolioScreen(name=name, currency=currency, value=value))
        self.sm.get_screen('main').ids['p_list'].add_widget(p_button)
        self.portfolio_buttons[name] = p_button


# -----------------  MainScreen  ----------------------------


class MainScreen(Screen):
    value = NumericProperty()
    currency = StringProperty()


class PortfolioButton(ButtonBehavior, MDBoxLayout):
    value = NumericProperty()

    def __init__(self, text, currency=Main().portfolios.currency, value=0, **kwargs):
        self.text = text
        self.currency = currency
        self.value = int(value)

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
            curr = MDApp.get_running_app().portfolios.currency

        if name:
            if name in MDApp.get_running_app().portfolios.instances.keys():
                p_name.error=True
                p_name.helper_text="{} has already been created".format(name)
            else:
                MDApp.get_running_app().portfolios.create_instance(name, currency=curr)
                MDApp.get_running_app().add_screen(name, currency=curr)
                self.dismiss()


# -----------------  PortfolioScreen  -----------------------


class PortfolioScreen(Screen):
    currency = ObjectProperty()
    value = NumericProperty()

    def __init__(self, currency, value, **kwargs):
        self.currency = currency
        self.value = int(value)
        super().__init__(**kwargs)

    def on_value(self, instance, value):
        MDApp.get_running_app().portfolios.update_value()
        MDApp.get_running_app().sm.get_screen('main').value = int(MDApp.get_running_app().portfolios.value)
        print('igy ok')

class NewTransaction(MDGridLayout):
    date = ObjectProperty()
    currency = ObjectProperty()
    type = ObjectProperty()
    amount = ObjectProperty()


class TransactionDialog(MDDialog):
    portfolio_name = None

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
        amount = float(self.content_cls.amount.text)
        transaction = {'date': date, 'currency': curr, 'type': type, 'amount': amount}
        MDApp.get_running_app().portfolios.instances[self.portfolio_name].cash.handle_transaction(transaction)
        MDApp.get_running_app().portfolios.instances[self.portfolio_name].update_value()
        MDApp.get_running_app().portfolio_buttons[self.portfolio_name].value = int(MDApp.get_running_app().portfolios.instances[self.portfolio_name].value)
        MDApp.get_running_app().sm.get_screen(self.portfolio_name).value = int(MDApp.get_running_app().portfolios.instances[self.portfolio_name].value)
        self.dismiss()


if __name__ == "__main__":
    Main().run()
