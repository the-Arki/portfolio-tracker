import pandas as pd
from datetime import datetime
from bond import Bond
from cash import Cash
from currency import Currency
from portfolio import Portfolio
from stock import Stock
import io_manager


class Portfolios:
    instances = {}

    def __init__(self):
        self.portfolio_names = io_manager.read_json(
            'files/portfolio_names.json')
        for name in self.portfolio_names:
            print("név az alején: ", name)
            self.instances[name] = Portfolio(name=name)

    def create_instance(self, name):
        self.portfolio_names.append(name)
        self.instances[name] = Portfolio(name=name)
        io_manager.write_json(self.portfolio_names, 'files/portfolio_names.json')

    def delete_instance(self, name):
        if name in self.portfolio_names:
            self.portfolio_names.remove(name)
            del self.instances[name]
            io_manager.write_json(self.portfolio_names, 'files/portfolio_names.json')
        else:
            print(f'{name} is not an instance.')

    def get_instance_values(self):
        # get the sum values of instances by type (stock, bond, cash)
        pass

    def calculate_total_value(self):
        # calculate the total value of the portfolios
        pass

###############################################################################
if __name__ == "__main__":
    tr1 = {"date": "2021-01-01", "type": 'Cash-In',
           "currency": "HUF", "amount": 10}
    tr2 = {"date": "2021-01-01", "type": 'Withdraw',
           "currency": "HUF", "amount": 10}
    tr3 = {"date": "2020-01-01", "type": 'Cash-In',
           "currency": "USD", "amount": 10}
    tr4 = {"date": "2019-01-01", "type": 'Cash-In',
           "currency": "HUF", "amount": 1}
    lista = ['kakas', 'birka']
    io_manager.write_json(lista, 'files/portfolio_names.json')
    x = Portfolios()
    print(x.instances)
    x.create_instance('kukorica')
    print(x.instances)
    x.delete_instance('kakas')
    print(x.instances)
    x.delete_instance('kakas')
    def handle_tr(name, transaction):
        x.instances[name].cash.handle_transaction(transaction)
        return x.instances[name].cash.cash_transactions_list
    # x.instances['birka'].cash.handle_transaction(tr1)
    def get_tot_value(name):
        total_value = x.instances[name].cash.get_total_value(x.instances[name].exchange_rates.currencies_df)
        return total_value
    ####################
    handle_tr('birka', tr1)
    tot1 = get_tot_value('birka')
    print(tot1)
    
    handle_tr('birka', tr2)
    print(handle_tr('birka', tr3))
    tot2 = get_tot_value('birka')
    print(tot2)
    print(x.instances['kukorica'].exchange_rates.currencies_df)
    print('név: ', x.instances["kukorica"].name)