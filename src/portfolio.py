from email import base64mime
import pandas as pd
from datetime import datetime
from bond import Bond
from cash import Cash
from stock import Stock
from currency import Currency


class Portfolio:
    """Collects a portfolio of the following elements:
        -Cash
        -Stock
        -Bond
    """
    today = str(datetime.date(datetime.now()))

    def __init__(self, currency="HUF", tr_dict={}, name=None):
        self.transactions_dict = self.setup_tr_dict(tr_dict)
        self.exchange_rates = Currency
        self.currency = currency
        self.bond = Bond(currency, tr_list=self.transactions_dict['Bond'], name=name)
        self.cash = Cash(currency, tr_list=self.transactions_dict['Cash'], name=name)
        self.name = name
        self.stock = Stock(currency, tr_list=self.transactions_dict['Stock'], name=name)
        self.set_currency(currency)

    def setup_tr_dict(self, tr_dict):
        if not tr_dict:
            for item in ('Bond', 'Cash', 'Stock'):
                tr_dict[item] = []
        return tr_dict

    def get_total_value(self, in_base_currency=True):
        base = in_base_currency
        items_list = [self.bond, self.cash, self.stock]
        df = pd.DataFrame()
        for item in items_list:
            print('item: {}'.format(item.__class__.__name__))
            if item.historical_df.empty:
                print('hat ez ures volt')
            else:
                df[item.__class__.__name__] = item.get_total_value(self.exchange_rates.currencies_df, in_base_currency=base)
                print('lefutott')
                df.append(df[item.__class__.__name__])
        total = df.sum(axis=1)
        return total

    def set_currency(self, currency):
        """set the currency for all the instances (bond, cash, stock),
        and updates the exchange rates accordingly in currency class.
        returns the new currency."""
        self.currency = currency
        for obj in [self.bond, self.cash, self.stock]:
            obj._currency = currency
        self.exchange_rates.set_exchange_rates(currency, self.today)
        return currency


# ------------------------------------------------------
if __name__ == "__main__":
    tr1 = {"date": "2021-01-01", "type": 'Cash-In',
           "currency": "EUR", "amount": 1000}
    tr2 = {"date": "2020-01-01", "type": 'Cash-In',
           "currency": "HUF", "amount": 10000}
    x = Portfolio()
    # print(Currency().currencies_df)
    x.cash.handle_transaction(tr1)
    # print(Currency().currencies_df)
    exch_df = Currency().currencies_df
    x.cash.get_total_value(exch_df)
    x.set_currency("EUR")
    x.cash.handle_transaction(tr2)
    exch_df = Currency().currencies_df
    x.cash.get_total_value(exch_df)
    print('ez az exchange db....................\n', Currency().currencies_df)
    x.get_total_value()
    print('---------------now with japanese yen-----------------------------')
    x.set_currency("JPY")
    x.cash.get_total_value(Currency().currencies_df)
    # print("just for fun\n", Currency().currencies_df)
    print(x.get_total_value())
