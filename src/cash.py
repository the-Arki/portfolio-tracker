from transactions import Transactions
import pandas as pd
from datetime import datetime


class Cash(Transactions):
    """
    Calculates the amount of available cash in the portfolio for each day.
    The currencies are handled separately
    and the transactions are collected in a list of dicts (cash_history).

    The history of the available amounts for every day is stored
    in a pandas DataFrame (cash_df).
    """

    def __init__(self, cash_df=pd.DataFrame, cash_transactions=None):
        self.cash_df = cash_df
        self.cash_transactions_list = cash_transactions

    # def sort_transactions_list(self):
    #     x = sorted(self.transactions_list,
    #                key=lambda transaction: transaction["date"])

    def add_transaction_to_df(self, transaction):
        tr = transaction
        if self.cash_df.empty:
            self.cash_df = self._create_dataframe(
                tr, first_creation=True)
            self.cash_df[tr["currency"]] = tr["amount"]
        else:
            if tr["date"] < str(self.cash_df.index[0]):
                temp_df = self._create_dataframe(tr)
                self.cash_df = pd.concat([temp_df, self.cash_df],
                                         copy=False, sort=True)
                self.cash_df.fillna(0, inplace=True)
            if tr["currency"] in self.cash_df.keys():
                self.cash_df.loc[self.cash_df.index >= tr["date"],
                                 tr['currency']] = self.cash_df[
                            tr["currency"]] + tr['amount']
            else:
                self.cash_df.loc[self.cash_df.index >= tr["date"],
                                 tr['currency']] = tr['amount']
                self.cash_df.fillna(0, inplace=True)
        return self.cash_df

    def _create_dataframe(self, transaction, first_creation=False):
        #  currently it works only for new cash_df
        #  temporary df is still missing
        start_date = transaction["date"]
        if first_creation:
            end_date = datetime.date(datetime.now())
        else:
            end_date = self.cash_df.index[0] - pd.Timedelta(days=1)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        df = pd.DataFrame(
            {transaction["currency"]: 0}, index=dates)
        return df


# -------------------------------------------------------------
tr1 = {"date": "2021-01-01", "currency": "HUF", "amount": 10}
tr2 = {"date": "2019-01-01", "currency": "HUF", "amount": 10}
tr3 = {"date": "2021-01-01", "currency": "USD", "amount": 10}
tr4 = {"date": "2019-01-01", "currency": "HUF", "amount": -3}
pesto = Cash()
pesto.add_transaction_to_df(tr1)
pesto.add_transaction_to_df(tr2)
pesto.add_transaction_to_df(tr3)
pesto.add_transaction_to_df(tr4)
for i in range(100):
    date = str(datetime(2019, 1, 1) + pd.Timedelta(days=i))
    pesto.add_transaction_to_df({"date": date, "currency": "EUR", "amount": 19})
print("df: ", pesto.cash_df)
