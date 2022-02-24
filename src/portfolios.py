import pandas as pd
from datetime import datetime
from bond import Bond
from cash import Cash
from currency import Currency
from portfolio import Portfolio
from stock import Stock


class Portfolios:
    portfolio_names = []
    portfolio_data = {}

    def __init__(self):
        for portfolio in self.portfolio_names:
            name = str(portfolio)
            portfolio = Portfolio()
            self.portfolio_data[name] = portfolio

    def get_instance(self, name):
        instance = self.portfolio_data[name]
        return instance
