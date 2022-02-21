import pandas as pd
from currency import Currency


class Stock():
    """
    """
    def __init__(self, currency="HUF", stock_df=pd.DataFrame()):
        self.historical_df = stock_df
        self.cash_transactions_list = []
        self._currency = currency
        self.exchange_rates = Currency()
