import pandas as pd
from datetime import datetime
from bond import Bond
from cash import Cash
from stock import Stock
from currency import Currency


class Portfolio():
    """Collects a portfolio of the following elements:
        -Cash
        -Stock
        -Bond
    """
    today = str(datetime.date(datetime.now()))

    def __init__(self, currency="HUF"):
        self.exchange_rates = Currency()
        self.currency = currency
        self.bond = Bond(currency)
        self.cash = Cash(currency)
        self.stock = Stock(currency)
        self.set_currency(currency)

    def get_total_value(self):
        items_list = [self.bond, self.cash, self.stock]
        df = pd.DataFrame()
        print(self.cash.historical_df)
        for item in items_list:
            print(item.historical_df)
            if not item.historical_df.empty:
                print(item.historical_df)
                df["yo"] = item.historical_df['Total'].copy()
                print('lefutott')
                print(item.historical_df)
            else:
                print('hat ez ures volt')

    def set_currency(self, currency):
        self.currency = currency
        for obj in [self.bond, self.cash, self.stock]:
            obj._currency = currency
        self.exchange_rates.set_exchange_rates(currency, self.today)
        return currency


# ------------------------------------------------------
tr1 = {"date": "2021-01-01", "type": 'Cash-In', "currency": "EUR", "amount": 1000}
x = Portfolio()
x.cash.handle_transaction(tr1)
exch_df = x.exchange_rates.currencies_df
print(exch_df)
print(x.cash.historical_df)
x.cash.get_total_value(exch_df)
x.get_total_value()
print(x.cash._currency)
x.change_currency("EUR")
print(x.cash._currency)