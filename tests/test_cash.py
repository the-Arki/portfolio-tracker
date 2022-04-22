from src.cash import Cash

cash = Cash()

transaction1 = {"date": "2020-02-22", "amount": 1, "currency": "HUF"}

class TestCash:
    def test__validate_transaction(self):
        assert True == cash._validate_transaction(transaction1)