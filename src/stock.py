import pandas as pd
from src.currency import Currency
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as web
import src.io_manager
import json
from src.transactions import Transactions
import requests

"""
to do list:
    sell equity
    by buy and sell the amount has to be subtracted from cash class!!!
    update stock price
    """


class Stock(Transactions):
    """
    """
    today = datetime.date(datetime.now())

    def __init__(self, currency="HUF", tr_list=[], name=None, type="ticker"):
        super().__init__(type)
        self.name = name
        self.historical_df = pd.DataFrame()
        self.stock_value_df = pd.DataFrame()
        self.transactions_list = tr_list
        if self.transactions_list:
            for item in self.transactions_list:
                self.historical_df = self._add_transaction_to_df(item, self.historical_df)
            self.stock_value_df = self.calculate_stock_value(self.historical_df)
        self._currency = currency
        self.exchange_rates = Currency().currencies_df

    def buy(self, date, ticker, amount, unit_price, fee, currency):
        """check if there is enough free cash in the portfolio.
        If so, then return the transaction in dictionary form.
        e.g. return {'ticker': 'MSFT', 'date': '2022-02-02', 'quantity': 6, 'price': 120, 'fee': 2, 'currency': 'USD'} """
        try:
            StockPrice.check_ticker(ticker)
        except (KeyError, IndexError):
            print('This ticker is not in our database')
            return None
        tr = self.handle_transaction(date, ticker, amount, unit_price, fee, currency, type="Buy")
        return tr

    def sell(self, date, ticker, amount, unit_price, fee, currency):
        """ Check if the quantity of the ticker in the portfolio is >= quantity.
        if so, then return the transaction in dictionary form.
        e.g. return {'ticker': 'MSFT', 'date': '2022-02-02', 'quantity': 6, 'price': 120, 'fee': 2, 'currency': 'USD'} """
        self.handle_transaction(date, ticker, amount, unit_price, fee, currency, type="Sell")

    def handle_transaction(self, date, ticker, amount, unit_price, fee, currency, type=None):
        tr = {"date": date, "ticker": ticker, "amount": amount,
              "unit_price": unit_price, "fee": fee, "type": type, "currency": currency}
        self.transactions_list = self.add_transaction_to_list(
                tr, self.transactions_list)
        self.save_transactions_list()
        self.historical_df = self._add_transaction_to_df(tr, self.historical_df)
        self.stock_value_df = self.calculate_stock_value(self.historical_df)
        total_price = unit_price * amount + fee
        transaction = {"date": date, "type": type, "currency": currency, "amount": total_price, "ticker": ticker}
        return transaction  # pass the returned transaction to cash class

    def calculate_stock_value(self, qty_df):
        df_raw = qty_df * StockPrice.stock_price_df[qty_df.columns]
        df_raw = df_raw.dropna(how='all')
        return df_raw

    def get_total_value(self, in_base_currency=True):
        """
        """
        if self.stock_value_df.empty:
            return None
        df = self.stock_value_df.copy()
        cols = []
        for i in df.columns:
            for item in StockPrice.stock_list:
                if item[0] == i:
                    cols.append(item[1])
        df_cur = df
        df_cur.columns = cols
        df_base = df_cur * self.exchange_rates[df_cur.columns]
        self.total_base_currency = df_base.sum(axis=1)
        self.total_actual_currency = self.total_base_currency.div(self.exchange_rates[self._currency])
        self.total_actual_currency.name = self._currency
        if in_base_currency:
            return self.total_base_currency
        return self.total_actual_currency


class StockPrice:
    """
    """
    try:
        stock_price_df = pd.read_csv('files/stock_prices.csv',
                                     parse_dates=True, header=[0], index_col=[0],
                                     skipinitialspace=True)
        stock_price_df.convert_dtypes(infer_objects=True)
        
    except (pd.errors.EmptyDataError, FileNotFoundError):
        stock_price_df = pd.DataFrame()
    try:
        stock_dict = io_manager.read_json('files/stock_prices_list.json')
        stock_list = [tuple(item) for item in stock_dict['tickers_list']]
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        stock_list = []
    today = datetime.date(datetime.now())

    @classmethod
    def check_ticker(cls, ticker):
        if ticker not in [item[0] for item in cls.stock_list]:
            currency = cls.get_ticker_currency(ticker)
            cls.add_to_list(ticker, currency)
            cls.stock_price_df = pd.concat([cls.stock_price_df, cls.add_stock_price(ticker)], axis=1)
            cls.save_df(cls.stock_price_df)
        else:
            print('{} is already in db'.format(ticker))
        return cls.stock_price_df

    @classmethod
    def get_ticker_currency(cls, ticker):
        url = 'https://query2.finance.yahoo.com/v7/finance/options/{}'.format(ticker)
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).json()
        info = response['optionChain']['result'][0]['quote']
        currency = info['currency']
        return currency

    @classmethod
    def add_to_list(cls, ticker, currency):
        cls.stock_list.append((ticker, currency))
        cls.save_list(cls.stock_list)

    @classmethod
    def save_list(cls, tickers_list):
        data = {}
        data['tickers_list'] = tickers_list
        io_manager.write_json(data, 'files/stock_prices_list.json')   

    @classmethod
    def add_stock_price(cls, ticker):
        start_date = cls.today - relativedelta(years=10)
        series = web.DataReader(ticker, data_source='yahoo', start=start_date, end=cls.today)['Adj Close']
        df = pd.DataFrame()
        df[ticker] = series
        df = df.loc[~df.index.duplicated()]
        df = df.dropna()
        return df

    @classmethod
    def save_df(cls, df):
        df.to_csv('files/stock_prices.csv')

    @classmethod
    def get_data(cls, ticker):
        d = web.get_data_yahoo_actions(ticker)
        return d
