import pandas as pd
from datetime import datetime
from src.bond import Bond
from src.cash import Cash
from src.stock import Stock
from src.currency import Currency


class Portfolio:
    """Collects a portfolio of the following elements:
        -Cash
        -Stock
        -Bond
    """
    today = str(datetime.date(datetime.now()))

    def __init__(self, currency="HUF", tr_dict={}, name=None):
        self.transactions_dict = self.setup_tr_dict(tr_dict)
        self.exchange_rates = Currency()
        self.currency = currency
        self.bond = Bond(currency, tr_list=self.transactions_dict['Bond'], name=name)
        self.cash = Cash(currency, tr_list=self.transactions_dict['Cash'], name=name)
        self.name = name
        self.stock = Stock(currency, tr_list=self.transactions_dict['Stock'], name=name)
        self.set_currency(currency)
        self.value = self.get_current_value(self.get_total_value(in_base_currency=False))

    def setup_tr_dict(self, tr_dict):
        if not tr_dict:
            for item in ('Bond', 'Cash', 'Stock'):
                tr_dict[item] = []
        return tr_dict

    def get_total_value(self, in_base_currency=True):
        items_list = [self.bond, self.cash, self.stock]
        df = pd.DataFrame()
        for item in items_list:
            if not item.historical_df.empty:
                df[item.__class__.__name__] = item.get_total_value()
                df.append(df[item.__class__.__name__])
        total = df.sum(axis=1)
        if in_base_currency:
            return total
        else:
            total_actual_currency = total.div(self.exchange_rates.currencies_df[self.currency])
            total_actual_currency.name = self.currency
            return total_actual_currency

    def get_current_value(self, df):
        if df.empty:
            return 0
        return df[-1]



    def set_currency(self, currency):
        """set the currency for all the instances (bond, cash, stock),
        and updates the exchange rates accordingly in currency class.
        returns the new currency."""
        self.currency = currency
        for obj in [self.bond, self.cash, self.stock]:
            obj._currency = currency
        self.exchange_rates.set_exchange_rates(currency, self.today)
        return currency
