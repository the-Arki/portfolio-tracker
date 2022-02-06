from transactions import Transactions

class Cash(Transactions):
    """Calculates the amount of available cash in the portfolio for each day.
    The separat currencies are handled separately and are collected in a list of dicts
    (cash_history)"""
    
    cash_history = []

    def sort_transactions_list(self):
        x = sorted(self.transactions_list, key=lambda transaction: transaction["date"])
        print(x)

Cash().sort_transactions_list()