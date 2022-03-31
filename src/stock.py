from pickletools import float8
import pandas as pd
from currency import Currency
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as web
import io_manager
import json
from transactions import Transactions
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

    def __init__(self, currency="HUF", stock_df=pd.DataFrame(), tr_list=[], name=None, type="ticker"):
        super().__init__(type)
        self.name = name
        self.historical_df = stock_df
        self.transactions_list = tr_list
        if self.transactions_list:
            for item in self.transactions_list:
                self.historical_df = self._add_transaction_to_df(item, self.historical_df)
        print(self.name, 'test stock df!!!!!!!!!!!!!!!!\n', self.historical_df)
        self._currency = currency
        self.exchange_rates = Currency().currencies_df
        self.stock_value_df = pd.DataFrame()

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
        self.calculate_stock_value(ticker)
        total_price = unit_price * amount + fee
        transaction = {"date": date, "type": type, "currency": currency, "amount": total_price, "ticker": ticker}
        return transaction  # pass the returned transaction to cash class

    def calculate_stock_value(self, ticker):
        price_df = StockPrice.check_ticker(ticker).copy()
        price_df.columns = price_df.columns.get_level_values('ticker')
        self.stock_value_df[ticker] = self.historical_df[ticker] * price_df[ticker]
        return self.stock_value_df









# ez jön most
    def get_total_value(self, in_base_currency=True):
        """
        """
        df = self.stock_value_df
        df = df.dropna(how='all')
        df['Total_base'] = df.sum(axis=1)
        df['Total'] = df['Total_base'].div(self.exchange_rates[self._currency])
        self.total_base_currency = pd.Series(df['Total_base'])
        if in_base_currency:
            return self.total_base_currency
        self.total_actual_currency = pd.Series(df['Total'])
        return self.total_actual_currency


class StockPrice:
    """
    """
    try:
        stock_price_df = pd.read_csv('files/stock_prices.csv',
                                     parse_dates=True, header=[0, 1], index_col=[0],
                                     skipinitialspace=True)
        stock_price_df.convert_dtypes(infer_objects=True)
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
        if ticker not in [key for d in cls.stock_list for key in d.keys()]:
            currency = cls.get_ticker_currency(ticker)
            cls.add_to_list(ticker, currency)
            cls.stock_price_df = pd.concat([cls.stock_price_df, cls.add_stock_price(ticker, currency)], axis=1)
            cls.save_df(cls.stock_price_df)
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
        cls.stock_list.append({ticker: currency})
        cls.save_list(cls.stock_list)

    @classmethod
    def save_list(cls, stickers_list):
        data = {}
        data['stickers_list'] = stickers_list
        io_manager.write_json(data, 'files/stock_prices_list.json')   

    @classmethod
    def add_stock_price(cls, ticker, currency):
        start_date = cls.today - relativedelta(years=10)
        series = web.DataReader(ticker, data_source='yahoo', start=start_date, end=cls.today)['Adj Close']
        df = pd.DataFrame(series)
        df.columns = pd.MultiIndex.from_tuples([(ticker, currency)], names=['ticker', 'currency'])
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

###################################################################
if __name__ == "__main__":
    StockPrice.check_ticker('TSLA')
    StockPrice.check_ticker('MSFT')
    try:
        StockPrice.check_ticker('kukorica')
    except (KeyError, IndexError):
        print('This ticker is not in our database')
    # print(StockPrice.stock_list)
    # print(StockPrice.stock_price_df)
    x = Stock(name="birka")
    x.buy("2022-02-22", "MSFT", 10, 305, 2, "USD")
