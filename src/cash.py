import pandas as pd
from datetime import datetime


class Cash():
    """
    Calculates the amount of available cash in the portfolio for each day.
    The currencies are handled separately
    and the transactions are collected in a list of dicts (cash_history).

    The history of the available amounts for every day is stored
    in a pandas DataFrame (cash_df).

    -get a transaction in dict format
    -validate it (the total amount for that currency cannot be less than 0)
        -it has to be checked for the whole column!!!
    -add the transaction to the cash_transactions_list
    -sort cash_transactions_list by date
    -update the database (cash_df) with the new value
    -add / update "total" column in database in the main currency (currency)
        -plot the cash history (cash_df["total"] column values)

    -edit transaction in transactions_list if needed
    """

    def __init__(self, currency="USD", cash_df=pd.DataFrame):
        self.cash_df = cash_df
        self.cash_transactions_list = []
        self.currency = currency

    def get_transaction(self, transaction):
        type = transaction["type"]
        add_list = ["Cash-In", "Dividend", "Sell"]
        subtract_list = ["Withdraw", "Buy"]
        transaction_ = transaction
        if type in add_list:
            transaction_["amount"] = transaction["amount"]
        elif type in subtract_list:
            transaction_["amount"] = -transaction["amount"]
        else:
            print('Transaction type ({}) is not defined.'.format(type))
            return None
        return transaction_

    def _validate_transaction(self, transaction):
        # this method should be changed
        if transaction["amount"] >= 0:
            return
        else:
            if (not self.cash_df.empty and
                transaction["currency"] in self.cash_df.columns and
                transaction["amount"] + (min(self.cash_df[transaction["currency"]].values)) >= 0):
                return
            else:
                print("There is not enough cash available for this transaction.")

    def add_transaction_to_list(self, transaction):
        self.cash_transactions_list.append(transaction)

    def remove_transaction(self, transaction):
        self.cash_transactions_list.remove(transaction)

    def edit_transaction(seld, transaction):
        pass

    def sort_transactions_list(self):
        self.cash_transactions_list = sorted(
            self.cash_transactions_list,
            key=lambda transaction: transaction["date"])

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
                                         copy=False, sort=True, axis=0)
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
        start_date = transaction["date"]
        if first_creation:
            end_date = datetime.date(datetime.now())
        else:
            end_date = self.cash_df.index[0] - pd.Timedelta(days=1)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        df = pd.DataFrame(
            {transaction["currency"]: 0}, index=dates)
        return df

    def get_total_value(self, currency_df):
        df = self.cash_df * currency_df[self.cash_df.columns]
        df = df.dropna(how='all')
        df['Total_USD'] = df.sum(axis=1)
        df['Total'] = df['Total_USD'].div(currency_df[self.currency])
        self.cash_df['Total'] = df['Total'].dropna(axis=1)
        return self.cash_df


# -------------------------------------------------------------
tr1 = {"date": "2021-01-10", "type": 'Cash-In', "currency": "HUF", "amount": 10}
tr2 = {"date": "2021-01-01", "type": 'Cash-In', "currency": "EUR", "amount": 10}
tr3 = {"date": "2020-01-01", "type": 'Cash-In', "currency": "USD", "amount": 10}
tr4 = {"date": "2019-01-01", "type": 'Withdraw', "currency": "HUF", "amount": 1}
pesto = Cash()


def test(tr):
    tr_ = pesto.get_transaction(tr)
    pesto._validate_transaction(tr_)
    pesto.add_transaction_to_df(tr_)
    print(pesto.cash_df)


test(tr1)
test(tr2)
test(tr3)
test(tr4)