from src.transactions import Transactions


trs = Transactions()


class TestTransactions:
    transaction = {"date": "2020-02-22", "amount": -1, "currency": "HUF"}
    tr_list = [{"date": "2022-03-22", "amount": -1, "currency": "HUF"}]

    def test_add_transaction_to_list(self):
        self.tr_list = trs.add_transaction_to_list(self.transaction, self.tr_list)
        assert self.tr_list == [
            {"date": "2020-02-22", "amount": -1, "currency": "HUF"},
            {"date": "2022-03-22", "amount": -1, "currency": "HUF"},
        ]
