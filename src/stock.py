import pandas as pd
from currency import Currency
from cash import Cash


class Stock():
    """
    """
    stock_price_df = pd.DataFrame() # it has to be loaded from file

    def __init__(self, currency="HUF", stock_df=pd.DataFrame(), tr_list=[], name=None):
        self.historical_df = stock_df
        self.transactions_list = tr_list
        self._currency = currency
        self.exchange_rates = Currency
        self.name = name

    def buy_equity(self, date, ticker, quantity, price, fee, currency, avaliable_cash):
        """check if there is enough free cash in the portfolio.
        If so, then return the transaction in dictionary form.
        e.g. return {'ticker': 'MSFT', 'date': '2022-02-02', 'quantity': 6, 'price': 120, 'fee': 2, 'currency': 'USD'} """
        pass

    def sell_equity(self, ticker, quantity, price, fee, currency):
        """Return the transaction in dictionary form.
        e.g. return {'ticker': 'MSFT', 'date': '2022-02-02', 'quantity': 6, 'price': 120, 'fee': 2, 'currency': 'USD'} """
        pass
