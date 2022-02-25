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
        for item in items_list:
            print('item: {}'.format(item.__class__.__name__))
            if item.historical_df.empty:
                print('hat ez ures volt')
            else:
                df[item.__class__.__name__] = item.total_actual_currency.copy()
                print('lefutott')
                df.append(df[item.__class__.__name__])
        total = df.sum(axis=1)
        return total

    def set_currency(self, currency):
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
    x.get_total_value()
