import pandas as pd
from currency import Currency


class Bond():
    """
    """
    def __init__(self, currency="HUF", bond_df=pd.DataFrame(), tr_list=[], name=None):
        self.historical_df = bond_df
        self.transactions_list = tr_list
        self._currency = currency
        self.exchange_rates = Currency()
        self.name = name
