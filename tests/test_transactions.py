import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
#------------------------------------------------------
from src.transactions import Transactions

trs = Transactions()

class TestTransactions():
    transaction = {"date": "2002", "amount": -1, "currency": "HUF"}

    def test_define_transaction(self):
        assert trs.define_transaction("2002", "Withdraw", 1, "HUF") == \
        {"date": "2002", "amount": -1, "currency": "HUF"}

    def test_add_transaction(self):
        new_item_to_add_to_transactions_list = trs.add_transaction(self.transaction)
        assert  self.transaction == trs.transactions_list[-1]