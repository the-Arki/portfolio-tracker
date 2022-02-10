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

    def __init__(self, cash_df=None, cash_transactions=None):
        self.cash_df = cash_df
        self.cash_transactions_list = cash_transactions

    # def sort_transactions_list(self):
    #     x = sorted(self.transactions_list,
    #                key=lambda transaction: transaction["date"])

    def _create_dataframe(self, transaction, end_date):
        #  currently it works only for new cash_df
        #  temporary df is still missing
        #  end_date might be sth else --> first_creation=False
        #  --> then call from add_tr...:
        # self._create_dataframe(transaction, first_creation=True)
        start_date = transaction["date"]
        end_date = end_date
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        self.cash_df = pd.DataFrame(
            {"date": dates, transaction["currency"]: transaction["amount"]})
        self.cash_df.set_index('date', inplace=True)

    def add_transaction_to_df(self, transaction):
        #  if not self.cash_df --> it might return sth else
        #  the rest of the function is incomplete
        if not self.cash_df:
            end_date = datetime.date(datetime.now())
            self._create_dataframe(transaction, end_date)
            return self.cash_df
        if transaction["date"] < str(self.cash_df.index[0]):
            dates_temp = self._create_dates(
                transaction["date"],
                self.cash_df.index[0] - pd.Timedelta(days=1))
            temp_df = pd.DataFrame({"date": dates_temp})
            temp_df.set_index("date", inplace=True)
            df = pd.concat([temp_df, self.cash_df], copy=False, sort=True)
        if transaction["currency"] in df.keys():
            df.fillna(0, inplace=True)
            df.loc[df.index >= transaction["date"], transaction['currency']] \
                = df[transaction["currency"]] + transaction['amount']
        else:
            df.loc[df.index >= transaction["date"], transaction['currency']] \
                = transaction['amount']


# -------------------------------------------------------------

"""
df = pd.DataFrame({'date': dates})

df.set_index('date', inplace=True)

# add a transaction {"date": 2021-01-01, "currency": "HUF", "amount": 10}
tr1 = {"date": "2021-01-01", "currency": "HUF", "amount": 10}
# if tr1["currency"] not in df.keys:
#     df[tr1["currency"]]


tr2 = {"date": "2019-01-01", "currency": "HUF", "amount": 10}
# add_tr_to_df(tr1)
# # print(df)
# add_tr_to_df(tr2)
# print("new_df: ", df)
"""
tr1 = {"date": "2021-01-01", "currency": "HUF", "amount": 10}
print(Cash().add_transaction_to_df(tr1))
