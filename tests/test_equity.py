from defer import return_value
from src.stock import Equity
from src.io_manager import read_json
import pytest


equity_info = read_json('./tests/equity_info.json')

equity = Equity('MSFT')

def test__get_info(mocker):
    mocker.patch('src.stock.Equity._get_info', return_value=equity_info)
    assert equity._get_info() == equity_info

def test_instance_info(mocker):
    mocker.patch('src.stock.Equity._get_info', return_value=equity_info)
    equity = Equity('MSFT')
    assert equity.info == equity_info

def test_instance_currency(mocker):
    mocker.patch('src.stock.Equity._get_info', return_value=equity_info)
    equity = Equity('MSFT')
    assert equity.currency == equity_info['currency']

def test_instance_tradeable(mocker):
    mocker.patch('src.stock.Equity._get_info', return_value=equity_info)
    equity = Equity('MSFT')
    assert equity.tradeable == equity_info['tradeable']
   
def test_tradeable():
    assert equity.is_tradeable() == equity_info['tradeable']

def test_tradeable_returns_boolean():
    assert isinstance(equity.is_tradeable(), bool)