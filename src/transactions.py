class Transactions():
    """It handles the transactions (cash-in/cash-out) of a portfolio.
    It's allowed to add / modify / delete transactions in the past or present,
    but not in the future."""

    def __init__(self):
        self.transactions_list = [
            {"date": "2002-02-22", "amount": 10, "currency": "HUF"},
            {"date": "2002-02-24", "amount": -1, "currency": "HUF"},
            {"date": "2002-02-22", "amount": 10, "currency": "USD"}]

    def define_transaction(self, date, type, amount, currency):
        if type in ["Cash-In", "Dividend"]:
            real_amount = amount
        if type == "Withdraw":
            real_amount = -amount
        transaction = {"date": date, "type": type, "amount": real_amount,
                       "currency": currency}
        return transaction

    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)

    def remove_transaction(self, transaction):
        self.transactions_list.remove(transaction)


if __name__ == "__main__":
    x = Transactions()
    tr = x.define_transaction('2020', "Withdraw", 20, 'HUF')
    x.add_transaction(tr)
    print(x.transactions_list)
