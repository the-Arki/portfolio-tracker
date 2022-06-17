import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, ScreenManagerException
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from src.main import Portfolios
from src.io_manager import save_plot

Window.size = (360, 640)
main_kv_file = "mainscreen.kv"


class MyScreenManager(ScreenManager):
    def change_screen(self, name):
        self.current = name


class Main(MDApp):
    portfolios = Portfolios()
    sm = MyScreenManager()
    portfolio_buttons = {}
    img = Texture.create()

    def build(self):
        self.load_kv(main_kv_file)
        value = int(self.portfolios.value)
        currency = self.portfolios.currency
        self.sm.add_widget(MainScreen(name="main", value=value, currency=currency))
        return self.sm

    def change_graph(self, name="main"):
        if name == "main":
            df = self.portfolios.calculate_total_value()
        else:
            df = self.portfolios.instances[name].get_total_value(in_base_currency=False)
        save_plot(name, df)
        self.sm.get_screen(name).ids.img.reload()

    def on_start(self):
        for name in self.portfolios.portfolio_names:
            currency = self.portfolios.instances[name].currency
            value = self.portfolios.instances[name].value
            self.add_screen(name, currency, value)

    def show_cash(self, name):
        df = self.portfolios.instances[name].cash.historical_df
        if not df.empty:
            for currency in df.columns:
                print("ez a {} utolso erteke".format(currency), df[currency][-1])

    def call_method(self, klass_, method_, **kwargs):
        klass = getattr(sys.modules[__name__], klass_)
        x = klass(**kwargs)
        method = getattr(x, method_)
        method()

    def add_screen(self, name, currency=portfolios.currency, value=0):
        p_button = PortfolioButton(text=name, currency=currency, value=value)
        self.sm.add_widget(PortfolioScreen(name=name, currency=currency, value=value))
        self.sm.get_screen(name).show_cash()
        self.sm.get_screen(name).show_stock()
        self.sm.get_screen("main").ids["p_list"].add_widget(p_button)
        self.portfolio_buttons[name] = p_button

    def create_screen(self, name, portfolio_name):
        self.sm.add_widget(BuyEquity(name=name, p_name=portfolio_name))
        self.sm.current = name


# -----------------  MainScreen  ----------------------------


class MainScreen(Screen):
    value = NumericProperty(None)
    currency = StringProperty()

    # def on_value(self, instance, value):
    #     try:
    #         MDApp.get_running_app().change_graph()
    #     except ScreenManagerException:
    #         pass


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
            "content_cls": AddPortfolio(),
            "title": "New transaction",
            "type": "custom",
            "buttons": [
                MDFlatButton(text="Cancel", on_release=lambda _: self.dismiss()),
                MDFlatButton(text="Add", on_release=lambda _: self.add_portfolio()),
            ],
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
                p_name.error = True
                p_name.helper_text = "{} has already been created".format(name)
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
        self.name = super().name

    def on_value(self, instance, value):
        MDApp.get_running_app().portfolios.update_value()
        MDApp.get_running_app().sm.get_screen("main").value = int(
            MDApp.get_running_app().portfolios.value
        )
        try:
            MDApp.get_running_app().change_graph(self.name)
        except ScreenManagerException:
            pass
        try:
            MDApp.get_running_app().change_graph()
        except ScreenManagerException:
            pass
        self.show_cash()
        self.show_stock()

    def show_cash(self):
        df = MDApp.get_running_app().portfolios.instances[self.name].cash.historical_df
        cash_dict = {}
        if not df.empty:
            for currency in df.columns:
                if int(df[currency][-1]):
                    cash_dict[currency] = int(df[currency][-1])
        else:
            cash_dict[""] = "No cash yet."
        self.ids.cash.clear_widgets()
        for k, v in cash_dict.items():
            self.ids.cash.add_widget(MDLabel(text=str(v)))
            self.ids.cash.add_widget(MDLabel(text=str(k)))

    def show_stock(self):
        stock = (
            MDApp.get_running_app().portfolios.instances[self.name].stock.historical_df
        )
        stock_value = (
            MDApp.get_running_app().portfolios.instances[self.name].stock.stock_value_df
        )
        self.ids.p_list.clear_widgets()
        for ticker in stock_value.columns:
            quantity = stock[ticker][-1]
            value = int(stock_value[ticker][-1])
            self.ids.p_list.add_widget(StockItems(ticker, quantity, value))


class StockItems(MDBoxLayout):
    ticker = ObjectProperty()
    quantity = ObjectProperty()
    value = ObjectProperty()

    def __init__(self, ticker, quantity, value, **kwargs):
        super().__init__(**kwargs)
        self.ticker = ticker
        self.quantity = quantity
        self.value = value


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
            "content_cls": NewTransaction(),
            "title": "New Transaction",
            "type": "custom",
            "buttons": [
                MDFlatButton(text="Cancel", on_release=lambda _: self.dismiss()),
                MDFlatButton(text="Add", on_release=lambda _: self.new_transaction()),
            ],
        }
        super().__init__(**kwargs)

    def new_transaction(self):
        date = self.content_cls.date.text
        curr = self.content_cls.currency.text
        type = self.content_cls.type.text
        amount = float(self.content_cls.amount.text)
        transaction = {"date": date, "currency": curr, "type": type, "amount": amount}
        MDApp.get_running_app().portfolios.instances[
            self.portfolio_name
        ].cash.handle_transaction(transaction)
        MDApp.get_running_app().portfolios.instances[self.portfolio_name].update_value()
        MDApp.get_running_app().portfolio_buttons[self.portfolio_name].value = int(
            MDApp.get_running_app().portfolios.instances[self.portfolio_name].value
        )
        MDApp.get_running_app().sm.get_screen(self.portfolio_name).value = int(
            MDApp.get_running_app().portfolios.instances[self.portfolio_name].value
        )
        self.dismiss()


class BuyEquity(Screen):
    date = ObjectProperty()
    ticker = ObjectProperty()
    amount = ObjectProperty()
    unit_price = ObjectProperty()
    fee = ObjectProperty()
    currency = ObjectProperty()

    def __init__(self, name, p_name, **kwargs):
        self.name = name
        self.portfolio_name = p_name
        super().__init__(**kwargs)

    def buy_equity(self):
        date = self.date.text
        ticker = self.ticker.text
        amount = float(self.amount.text)
        unit_price = float(self.unit_price.text)
        fee = float(self.fee.text)
        currency = self.currency.text
        MDApp.get_running_app().portfolios.instances[self.portfolio_name].buy_equity(
            date, ticker, amount, unit_price, fee, currency
        )
        MDApp.get_running_app().portfolios.instances[self.portfolio_name].update_value()
        MDApp.get_running_app().portfolio_buttons[self.portfolio_name].value = int(
            MDApp.get_running_app().portfolios.instances[self.portfolio_name].value
        )
        MDApp.get_running_app().sm.get_screen(self.portfolio_name).value = int(
            MDApp.get_running_app().portfolios.instances[self.portfolio_name].value
        )
        MDApp.get_running_app().sm.current = self.portfolio_name


if __name__ == "__main__":
    Main().run()
