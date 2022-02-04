"""
Transaction class of this module handles the transactions (cash-in/cash-out) of a portfolio.
You are allowed to add / modify / delete transactions in the past or present, but not in the future.
"""

class Transactions():
    transactions_list = []
    
    def add_transaction(self, date, type, amount, currency):
        if type == "Cash-In":
            real_amount = amount
        if type == "Withdraw":
            real_amount = -amount
        transaction = {"date": date, "amount": real_amount, "currency": currency}
        self.transactions_list.append(transaction)
        return transaction

test = Transactions()
test.add_transaction("2020.01.20.", "Withdraw", 1200, "HUF")
test.add_transaction("2020.01.20.", "Cash-In", 1200, "HUF")
print(test.transactions_list)