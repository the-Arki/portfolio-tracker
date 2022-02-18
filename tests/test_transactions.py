from src.transactions import Transactions


trs = Transactions()


class TestTransactions():
    transaction = {"date": "2002", "amount": -1, "currency": "HUF"}

    def test_define_transaction(self):
        assert trs.define_transaction("2002", "Withdraw", 1, "HUF") == \
        {"date": "2002", "type": "Withdraw", "amount": -1, "currency": "HUF"}

    def test_add_transaction(self):
        trs.add_transaction(self.transaction)
        assert self.transaction == trs.transactions_list[-1]
