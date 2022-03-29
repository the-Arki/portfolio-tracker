import pandas as pd
from datetime import datetime


class Transactions:
    """
    """
    def _add_transaction_to_df(self, transaction, df, name="currency"):
        """example_transaction = {
            "date": "2022-03-21",
            "type": 'Cash-In',
            "currency": "HUF",
            "amount": 10}
           """
        tr = transaction
        if df.empty:
            df = self._create_dataframe(tr, first_creation=True)
            df[tr[name]] = tr["amount"]
        else:
            if tr["date"] < str(df.index[0]):
                temp_df = self._create_dataframe(tr)
                df = pd.concat([temp_df, df], copy=False, sort=True, axis=0)
                df = df.fillna(0)
            if tr[name] in df.keys():
                df.loc[df.index >= tr["date"], tr[name]] = (
                    df[tr[name]] + tr['amount'])
            else:
                df.loc[df.index >= tr["date"], tr[name]] = tr['amount']
                df.fillna(0)
        return df

    def _create_dataframe(self, transaction, first_creation=False):
        start_date = transaction["date"]
        if first_creation:
            end_date = self.today
        else:
            end_date = self.historical_df.index[0] - pd.Timedelta(days=1)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        df = pd.DataFrame(
            {transaction["currency"]: 0}, index=dates)
        return df

    def _sort_transactions_list(self, tr_list):
        tr_list_sorted = sorted(tr_list, key=lambda transaction: transaction["date"])
        return tr_list_sorted
