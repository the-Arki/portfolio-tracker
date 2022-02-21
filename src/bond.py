import pandas as pd
from currency import Currency


class Bond():
    """
    """
    def __init__(self, currency="HUF", bond_df=pd.DataFrame()):
        self.historical_df = bond_df
        self.cash_transactions_list = []
        self._currency = currency
        self.exchange_rates = Currency()
