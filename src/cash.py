import pandas as pd
from datetime import datetime
from currency import Currency


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
    -update exchange rates in Currency class --> _update_exchange_rates
        -edit transaction in transactions_list if needed
    """

    def __init__(self, currency="HUF", cash_df=pd.DataFrame()):
        self.historical_df = cash_df
        self.cash_transactions_list = []
        self._currency = currency
        self.exchange_rates = Currency()

    def handle_transaction(self, transaction):
        tr = self._get_transaction(transaction)
        if not tr:
            return
        if self._validate_transaction(tr):
            self.add_transaction_to_list(tr)
            self._sort_transactions_list()
            self._add_transaction_to_df(tr)
            self._update_exchange_rates(tr)
        else:
            return

    def _get_transaction(self, transaction):
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
            return True
        else:
            if (not self.historical_df.empty and
                transaction["currency"] in self.historical_df.columns and
                transaction["amount"] + (min(self.historical_df[transaction["currency"]].values)) >= 0):
                return True
            else:
                print("There is not enough cash available for this transaction.")
                while True:
                    decision = input("Test it? (Yes or No)")
                    if decision.lower() == "yes":
                        return True
                    elif decision.lower() == "no":
                        return False
                    else:
                        print("TypeError - The answer {} is incorrect.".format(decision))

    def add_transaction_to_list(self, transaction):
        # not done yet
        self.cash_transactions_list.append(transaction)

    def remove_transaction(self, transaction):
        # not done yet
        self.cash_transactions_list.remove(transaction)

    def edit_transaction(seld, transaction):
        # not done yet
        pass

    def _sort_transactions_list(self):
        self.cash_transactions_list = sorted(
            self.cash_transactions_list,
            key=lambda transaction: transaction["date"])

    def _add_transaction_to_df(self, transaction):
        tr = transaction
        if self.historical_df.empty:
            self.historical_df = self._create_dataframe(
                tr, first_creation=True)
            self.historical_df[tr["currency"]] = tr["amount"]
        else:
            if tr["date"] < str(self.historical_df.index[0]):
                temp_df = self._create_dataframe(tr)
                self.historical_df = pd.concat([temp_df, self.historical_df],
                                               copy=False, sort=True, axis=0)
                self.historical_df.fillna(0, inplace=True)
            if tr["currency"] in self.historical_df.keys():
                self.historical_df.loc[self.historical_df.index >= tr["date"],
                                       tr['currency']] = self.historical_df[
                            tr["currency"]] + tr['amount']
            else:
                self.historical_df.loc[self.historical_df.index >= tr["date"],
                                       tr['currency']] = tr['amount']
                self.historical_df.fillna(0, inplace=True)
        return self.historical_df

    def _create_dataframe(self, transaction, first_creation=False):
        start_date = transaction["date"]
        if first_creation:
            end_date = datetime.date(datetime.now())
        else:
            end_date = self.historical_df.index[0] - pd.Timedelta(days=1)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        df = pd.DataFrame(
            {transaction["currency"]: 0}, index=dates)
        return df

    def _update_exchange_rates(self, transaction):
        self.exchange_rates.set_exchange_rates(transaction["currency"],
                                               transaction["date"])

    def get_total_value(self, currency_df):
        df = self.historical_df * currency_df[self.historical_df.columns]
        df = df.dropna(how='all')
        df['Total_base'] = df.sum(axis=1)
        df['Total'] = df['Total_base'].div(currency_df[self._currency])
        # self.historical_df['Total'] = df['Total']
        self.total_base_currency = pd.Series(df['Total_base'])
        self.total_actual_currency = pd.Series(df['Total'])
        return self.total_actual_currency


# -------------------------------------------------------------
if __name__ == "__main__":
    tr1 = {"date": "2021-01-01", "type": 'Cash-In', "currency": "HUF", "amount": 10}
    tr2 = {"date": "2021-01-01", "type": 'Cash-In', "currency": "HUF", "amount": 10}
    tr3 = {"date": "2020-01-01", "type": 'Cash-In', "currency": "USD", "amount": 10}
    tr4 = {"date": "2019-01-01", "type": 'Cash-In', "currency": "HUF", "amount": 1}
    pesto = Cash()

    def test(tr):
        pesto.handle_transaction(tr)
    test(tr1)
    test(tr2)
    test(tr3)
    test(tr4)
    print("df at the end: ", pesto.historical_df)
    test_df = pesto.exchange_rates.currencies_df
    x = pesto.get_total_value(test_df)
    print("yooooooooooooooooooooooooooo", x)
