import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from src.bond import Bond
from src.cash import Cash
from src.currency import Currency
from src.portfolio import Portfolio
from src.stock import Stock, StockPrice
import src.io_manager as io_manager
import json


class Portfolios:
    instances = {}

    def __init__(self, currency="HUF"):
        self.currency = currency
        Currency().update_df()
        try:
            self.all_transactions = io_manager.read_json('files/transactions.json')
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            self.all_transactions = {}
        try:
            self.portfolio_names = io_manager.read_json(
                'files/portfolio_names.json')
            for name in self.portfolio_names.keys():
                self.instances[name] = Portfolio(tr_dict=self.all_transactions[name], name=name, currency=self.portfolio_names[name])
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            print('no portfolio has been created yet')
            self.portfolio_names = {}
        self.value = self.get_current_value(self.calculate_total_value())

    def create_instance(self, name, currency):
        if name in self.portfolio_names.keys():
            print('instance already exists')
            return
        self.portfolio_names[name] = currency
        self.save_new_transactions(name)
        self.instances[name] = Portfolio(tr_dict=self.all_transactions[name], name=name, currency=currency)
        io_manager.write_json(self.portfolio_names, 'files/portfolio_names.json')

    def delete_instance(self, name):
        if name in self.portfolio_names:
            self.portfolio_names.remove(name)
            del self.instances[name]
            io_manager.write_json(self.portfolio_names, 'files/portfolio_names.json')
            self.save_del_transactions(name)
        else:
            print(f'{name} is not an instance.')

    def save_new_transactions(self, name):
        self.all_transactions[name] = {'Bond': [], 'Cash': [], 'Stock': []}
        io_manager.write_json(self.all_transactions, 'files/transactions.json')

    def save_del_transactions(self, name):
        del self.all_transactions[name]
        io_manager.write_json(self.all_transactions, 'files/transactions.json')

    def get_instance_values(self):
        # get the sum values of instances by type (stock, bond, cash)
        pass

    def buy_equity(self, name, date, ticker, amount, unit_price, fee, currency):
        total_amount = amount * unit_price + fee
        tr = {"date": date, "currency": currency, "amount": total_amount}
        if self.instances[name].cash._validate_transaction(tr):
            transaction = self.instances[name].stock.buy(date, ticker, amount, unit_price, fee, currency)
            if transaction:
                self.instances[name].cash.handle_transaction(transaction)
        else:
            print("There is not enough cash available for this transaction.")

    def calculate_total_value(self):
        """get the total values of the individual portfolios in base currency
        and return the sum of the total values in main currency."""
        df = pd.DataFrame()
        for name, obj in self.instances.items():
            df[name] = obj.get_total_value()
        total_base = df.sum(axis=1)
        total = total_base.div(Currency().currencies_df[self.currency])
        total = total.dropna(how='all')
        return total

    def get_current_value(self, df):
        if df.empty:
            return 0
        return df[-1]

    def update_value(self):
        self.value = self.get_current_value(self.calculate_total_value())

    def plot(self, name):
        df = self.calculate_total_value()
        df.plot(kind='line')
        plt.savefig('./files/images/' + name + '_graph.png')
        plt.close()

if __name__ == "__main__":
    x = Portfolios()
