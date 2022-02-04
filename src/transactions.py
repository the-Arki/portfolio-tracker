"""
Transactions class of this module handles the transactions (cash-in/cash-out) of a portfolio.
You are allowed to add / modify / delete transactions in the past or present, but not in the future.
"""

class Transactions():
    transactions_list = []
    
    def define_transaction(self, date, type, amount, currency):
        if type == "Cash-In":
            real_amount = amount
        if type == "Withdraw":
            real_amount = -amount
        transaction = {"date": date, "amount": real_amount, "currency": currency}
        return transaction
    
    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)
    
    def remove_transaction(self, transaction):
        self.transactions_list.remove(transaction)