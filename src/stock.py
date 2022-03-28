import pandas as pd
from currency import Currency
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as web
import io_manager
import json

"""
to do list:
    save stock price df to file
    load data from this file at init
    buy equity
    sell equity
    update stock price
    """


class Stock:
    """
    """
    stock_value_df = pd.DataFrame()  # it has to be loaded from file
    today = datetime.date(datetime.now())

    def __init__(self, currency="HUF", stock_df=pd.DataFrame(), tr_list=[], name=None):
        self.historical_df = stock_df
        self.transactions_list = tr_list
        self._currency = currency
        self.exchange_rates = Currency().currencies_df
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


class StockPrice:
    """
    """
    try:
        stock_price_df = pd.read_csv('files/stock_prices.csv',
                                     parse_dates=True, index_col=[0])
    except (pd.errors.EmptyDataError, FileNotFoundError):
        stock_price_df = pd.DataFrame()
    try:
        stock_dict = io_manager.read_json('files/stock_prices_list.json')
        stock_list = stock_dict['stickers_list']
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        stock_list = []
    today = datetime.date(datetime.now())

    @classmethod
    def check_ticker(cls, ticker):
        print(cls.stock_list)
        if ticker not in cls.stock_list:
            cls.add_to_list(ticker)
            cls.stock_price_df[ticker] = cls.add_stock_price(ticker)
            cls.save_df(cls.stock_price_df)

    @classmethod
    def add_to_list(cls, ticker):
        cls.stock_list.append(ticker)
        cls.save_list(cls.stock_list)

    @classmethod
    def save_list(cls, stickers_list):
        data = {}
        data['stickers_list'] = stickers_list
        io_manager.write_json(data, 'files/stock_prices_list.json')
        

    @classmethod
    def add_stock_price(cls, ticker):
        start_date = cls.today + relativedelta(years=-10)
        df = web.DataReader(ticker, data_source='yahoo', start=start_date, end=cls.today)['Adj Close']
        return df

    @classmethod
    def save_df(cls, df):
        df.to_csv('files/stock_prices.csv')


###################################################################
if __name__ == "__main__":
    StockPrice.check_ticker('TSLA')
    print(StockPrice.stock_list)
    print(StockPrice.stock_price_df)
