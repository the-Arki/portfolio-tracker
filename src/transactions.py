import pandas as pd
from datetime import datetime


class Transactions:
    """
    """
    def _add_transaction_to_df(self, transaction, df, type="currency"):
        tr = transaction
        if df.empty:
            df = self._create_dataframe(tr, first_creation=True)
            df[tr[type]] = tr["amount"]
        else:
            if tr["date"] < str(df.index[0]):
                temp_df = self._create_dataframe(tr)
                df = pd.concat([temp_df, df], copy=False, sort=True, axis=0)
                df = df.fillna(0)
            if tr[type] in df.keys():
                df.loc[df.index >= tr["date"], tr[type]] = (
                    df[tr[type]] + tr['amount'])
            else:
                df.loc[df.index >= tr["date"], tr[type]] = tr['amount']
                df.fillna(0)
        return df

    def _sort_transactions_list(self, tr_list):
        tr_list_sorted = sorted(tr_list, key=lambda transaction: transaction["date"])
        return tr_list_sorted
