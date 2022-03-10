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
            self.instances[name] = Portfolio()

    def create_instance(self, name):
        self.portfolio_names.append(name)
        self.instances[name] = Portfolio()
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
lista = ['kakas', 'birka']
io_manager.write_json(lista, 'files/portfolio_names.json')
x = Portfolios()
print(x.instances)
x.create_instance('kukorica')
print(x.instances)
x.delete_instance('kakas')
print(x.instances)
x.delete_instance('kakas')