import pandas as pd
from datetime import datetime
from bond import Bond
from cash import Cash
from currency import Currency
from portfolio import Portfolio
from stock import Stock
import io_manager
import json


class Portfolios:
    instances = {}

    def __init__(self, currency="HUF"):
        self.currency = currency
        try:
            self.all_transactions = io_manager.read_json('files/transactions.json')
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            self.all_transactions = {}
        try:
            self.portfolio_names = io_manager.read_json(
                'files/portfolio_names.json')
            for name in self.portfolio_names:
                self.instances[name] = Portfolio(tr_dict=self.all_transactions[name], name=name)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            print('no portfolio has been created yet')
            self.portfolio_names = []

    def create_instance(self, name):
        if name in self.portfolio_names:
            print('instance already exists')
            return
        self.portfolio_names.append(name)
        self.save_new_transactions(name)
        self.instances[name] = Portfolio(tr_dict=self.all_transactions[name], name=name)
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

    def calculate_total_value(self):
        """get the total values of the portfolios in base currency
        and return the sum of the total values in main currency."""
        df = pd.DataFrame()
        for name, obj in self.instances.items():
            df[name] = obj.get_total_value()
        total_base = df.sum(axis=1)
        total = total_base.div(Currency().currencies_df[self.currency])
        total = total.dropna(how='all')
        return total


###############################################################################
if __name__ == "__main__":
    tr1 = {"date": "2022-03-21", "type": 'Cash-In',
           "currency": "HUF", "amount": 220}
    tr2 = {"date": "2022-03-22", "type": 'Withdraw',
           "currency": "HUF", "amount": 10}
    tr3 = {"date": "2022-03-19", "type": 'Cash-In',
           "currency": "USD", "amount": 10}
    tr4 = {"date": "2022-03-15", "type": 'Cash-In',
           "currency": "EUR", "amount": 1}
    # lista = ['kakas', 'birka']
    # io_manager.write_json(lista, 'files/portfolio_names.json')
    x = Portfolios()
    print(x.instances)
    # x.create_instance('birka')
    # print(x.instances)
    # x.delete_instance('kakas')
    # print(x.instances)
    # x.delete_instance('kakas')
    def handle_tr(name, transaction):
        x.instances[name].cash.handle_transaction(transaction)
        return x.instances[name].cash.cash_transactions_list
    # x.instances['birka'].cash.handle_transaction(tr1)
    def get_tot_value(name):
        total_value = x.instances[name].cash.get_total_value(in_base_currency=False)
        return total_value
    # ####################
    # handle_tr('birka', tr1)
    tot1 = get_tot_value('kukorica')
    print(tot1)
    print('na ez most portfolio total')
    print(x.instances['birka'].name)
    print(x.calculate_total_value())
    # x.create_instance('kukorica')
    # handle_tr('birka', tr2)
    # print(handle_tr('birka', tr3))
    # handle_tr('kukorica', tr4)
    # tot2 = get_tot_value('birka')
    # print("ez a tot2: ", tot2)
    # print(x.instances['kukorica'].exchange_rates.currencies_df)
    # print('név: ', x.instances["kukorica"].name)
    print(x.instances['kukorica'].transactions_dict)
    