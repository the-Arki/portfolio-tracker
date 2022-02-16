import pandas as pd
from pandas_datareader import data as web
from datetime import datetime


class Currency():
    """
    methods required to complete the basic class:
        -if currencies_df = None:
            -create currencies_df when needed
    """
    """
    This class converts the used currencies to a base currency and from there
    to the required one.

    The currency pairs are stored in a pandas DataFrame (currencies_df)

    programm starts (at least the first time) without any data, therefore
    currencies_df is an empty DataFrame (no start date defined)
    whenever the start_date changes from None to a date:
        -add 'currency' column to df with startdate and with today as enddate
        -get exchange rates for currency to base_currency pairs
            and store them in a DataFrame (currencies_df)
        -if the start_date < previous start_date:
            -update dataframe with the missing values
    """
    base_currency = 'USD'
    today = datetime.date(datetime.now())

    def __init__(self, start_date=None, currencies_df=pd.DataFrame):
        self.currencies_df = currencies_df
        self.start_date = start_date

    def _check_currency(self, currency):
        """Check if currency is in the exchange rates database and
        return a boolean"""

        if self.currencies_df.empty:
            return False
        elif currency not in self.currencies_df.columns:
            return False
        else:
            return True

    def _create_dataframe(self):
        "create a dataframe for exchange rates if it is not existing yet."

        dates = pd.date_range(start=self.start_date, end=self.today, freq='D')
        self.currencies_df = pd.DataFrame(index=dates)
        return self.currencies_df

    def set_exchange_rates(self, currency, start_date):
        """Set the exchange range for the passed currency.
        If the given start date is earlier than the current self.start_date,
        then update all values with this new start.
        """
        if self.currencies_df.empty:
            self._create_dataframe()
        if not self._check_currency(currency):
            self._add_currency_to_df(currency)
        if start_date < self.start_date:
            self._update_df()
        return self.currencies_df

    def _add_currency_to_df(self, currency):
        """Add the currency to the exchange database.
        If the first value is NaN, then look for an earlier value to start.
        """
        self.currencies_df[currency] = (
            web.DataReader(currency + self.base_currency + '=X',
                           data_source='yahoo', start=self.start_date,
                           end=self.today)['Adj Close'])
        self.currencies_df[currency].ffill(inplace=True)
        days_back = 1
        # if the exchange rate is 0 at self.start_date then look for the 
        # first non 0 value for that day
        while pd.isna(self.currencies_df.loc[self.start_date, currency]):
            start_date_ = pd.to_datetime(self.start_date) - pd.Timedelta(
                days=days_back)
            end_date_ = start_date_ + pd.Timedelta(days=1)
            start_date_str = start_date_.strftime('%Y-%m-%d')
            end_date_str = end_date_.strftime('%Y-%m-%d')
            df = (web.DataReader(currency + self.base_currency + '=X',
                                 data_source='yahoo', start=start_date_str,
                                 end=end_date_str)['Adj Close'])
            if df.index[0] != start_date_:
                days_back += 1
            else:
                self.currencies_df.loc[self.start_date, currency] = (
                    df.iloc[0])
        return self.currencies_df

    def _update_df(self):
        # set xchange rates for the missing dates
        # if there is no xchange rate for the first date:
        #   look for the previous dates until there is a value
        pass


c = Currency(start_date='2020-12-27')
print(c.today)
c.set_exchange_rates('HUF', '2021-12-31')
print(c.currencies_df)
c.set_exchange_rates('EUR', '2020-01-01')
print(c.currencies_df)
