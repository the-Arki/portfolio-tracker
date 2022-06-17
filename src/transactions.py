import pandas as pd
from datetime import datetime
from src.io_manager import read_json, write_json


class Transactions:
    """ """

    def __init__(self, type="currency"):
        self.type = type

    def add_transaction_to_list(self, transaction, tr_list):
        tr_list.append(transaction)
        sorted_list = sorted(tr_list, key=lambda transaction: transaction["date"])
        return sorted_list

    def save_transactions_list(self):
        tr_dict = read_json("files/transactions.json")
        tr_dict[self.name][self.__class__.__name__] = self.transactions_list
        write_json(tr_dict, "files/transactions.json")

    def _add_transaction_to_df(self, transaction, df):
        """example_transaction = {
        "date": "2022-03-21",
        "type": 'Sell',
        "currency": "HUF",
        "amount": 10}
        """
        tr = transaction
        if df.empty:
            df = self._create_dataframe(tr, first_creation=True)
            df[tr[self.type]] = tr["amount"]
        else:
            if tr["date"] < str(df.index[0]):
                temp_df = self._create_dataframe(tr)
                df = pd.concat([temp_df, df], copy=False, sort=True, axis=0)
                df = df.fillna(0)
            if tr[self.type] in df.keys():
                df.loc[df.index >= tr["date"], tr[self.type]] = (
                    df[tr[self.type]] + tr["amount"]
                )
            else:
                df.loc[df.index >= tr["date"], tr[self.type]] = tr["amount"]
                df.fillna(0)
        return df

    def _create_dataframe(self, transaction, first_creation=False):
        type = self.type
        start_date = transaction["date"]
        if first_creation:
            end_date = self.today
        else:
            end_date = self.historical_df.index[0] - pd.Timedelta(days=1)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        df = pd.DataFrame({transaction[type]: 0}, index=dates)
        return df
