import pandas as pd
from datetime import datetime
from src.currency import Currency
from src.io_manager import read_json, write_json
from src.transactions import Transactions


class Cash(Transactions):
    """
    Calculates the amount of available cash in the portfolio for each day.
    The currencies are handled separately
    and the transactions are collected in a list of dicts (cash_history).

    The history of the available amounts for every day is stored
    in a pandas DataFrame (cash_df).

    -get a transaction in dict format
    -validate it (the total amount for that currency cannot be less than 0)
     -it has to be checked for the whole column!!!
        -add the transaction to the transactions_list
    -sort transactions_list by date
    -update the database (cash_df) with the new value
    -add / update "total" column in database in the main currency (currency)
    -update exchange rates in Currency class --> _set_exchange_rates
        -edit transaction in transactions_list if needed
    """
    today = datetime.date(datetime.now())

    def __init__(self, currency="HUF", cash_df=pd.DataFrame(), tr_list=[], name=None):
        super().__init__()
        self.historical_df = cash_df
        self.transactions_list = tr_list
        if self.transactions_list:
            for item in self.transactions_list:
                self.historical_df = self._add_transaction_to_df(
                    item, self.historical_df)
        self._currency = currency
        self.exchange_rates = Currency().currencies_df
        self.name = name

    def handle_transaction(self, transaction):
        tr = self._get_transaction(transaction)
        if not tr:
            return
        if self._validate_transaction(tr):
            self.transactions_list = self.add_transaction_to_list(
                tr, self.transactions_list)
            self.save_transactions_list()
            self.historical_df = self._add_transaction_to_df(
                tr, self.historical_df)
            self._set_exchange_rates(tr)
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
        tr = transaction
        if tr["amount"] >= 0:
            return True
        else:
            if (not self.historical_df.empty and
                tr["currency"] in self.historical_df.columns and
                (tr["amount"] +
                 (min(self.historical_df.loc[self.historical_df.index >= tr["date"], tr["currency"]])) >= 0)):
                return True
            else:
                print("Not enough cash available for this transaction.")
                while True:
                    decision = input("Test it? (Yes or No)")
                    if decision.lower() == "yes":
                        return True
                    elif decision.lower() == "no":
                        return False
                    else:
                        print(("TypeError - The answer {} is incorrect."
                               .format(decision)))

    def remove_transaction(self, transaction):
        # not done yet
        self.transactions_list.remove(transaction)

    def edit_transaction(seld, transaction):
        # not done yet
        pass

    def _set_exchange_rates(self, transaction):
        Currency().set_exchange_rates(transaction["currency"],
                                      transaction["date"])

    def update_historical_df(self, df):
        end_date = self.today
        if df.index[-1] < end_date:
            df = df.ffill()
        return df

    def get_total_value(self, in_base_currency=True):
        """get exchange rates df from currency class as 'currency_df' and 
        optionally in_base_currency.
        returns the total cash value of the instance in base currency (USD) or
        in the actual currency of the instance if 'in_base_currency' is set to False"""
        df = self.historical_df * self.exchange_rates[self.historical_df.columns]
        df = df.dropna(how='all')
        df['Total_base'] = df.sum(axis=1)
        df['Total'] = df['Total_base'].div(self.exchange_rates[self._currency])
        self.total_base_currency = pd.Series(df['Total_base'])
        if in_base_currency:
            return self.total_base_currency
        self.total_actual_currency = pd.Series(df['Total'])
        return self.total_actual_currency
