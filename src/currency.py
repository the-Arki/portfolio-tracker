import pandas as pd
from pandas_datareader import data as web
from datetime import datetime


class Currency():
    """
    This class converts the used currencies to a base currency and from there
    to the required one.

    The currency pairs are stored in a pandas DataFrame (currencies_df)

    program starts (at least the first time) without any data, therefore
    currencies_df is an empty DataFrame (no start date defined)
    whenever the start_date changes from None to a date:
        -add 'currency' column to df with startdate and with today as enddate
        -get exchange rates for currency to _base_currency pairs
            and store them in a DataFrame (currencies_df)
        -if the start_date < previous start_date:
            -update dataframe with the missing values
    """
    _base_currency = 'USD'
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

    def _create_dataframe(self, start_date, end_date):
        "create a dataframe for exchange rates if it is not existing yet."
        start_date = start_date
        end_date = end_date
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        df = pd.DataFrame(index=dates)
        return df

    def set_exchange_rates(self, currency, start_date):
        """Set the exchange range for the passed currency.
        If the given start date is earlier than the current self.start_date,
        then update all values with this new start.
        """
        if not self.start_date:
            self.start_date = start_date
        if self.currencies_df.empty:
            self.currencies_df = self._create_dataframe(self.start_date,
                                                        self.today)
        if not self._check_currency(currency):
            self.currencies_df = (
                self._add_currency_to_df(currency, self.currencies_df,
                                         self.start_date, self.today))
        if start_date < self.start_date:
            self.currencies_df = self._update_df(start_date, self.start_date,
                                                 self.currencies_df)
        return self.currencies_df

    def _add_currency_to_df(self, currency, df, start_date, end_date):
        """Add the currency to the exchange rates database.
        If the first value is NaN, then look for an earlier value to start.
        """
        df[currency] = (web.DataReader(currency + self._base_currency + '=X',
                        data_source='yahoo', start=start_date,
                        end=end_date)['Adj Close'])
        if pd.isna(df.loc[start_date, currency]):
            df.loc[start_date, currency] = (
                self._get_first_value(currency, start_date))
        df[currency].ffill(inplace=True)
        return df

    def _get_first_value(self, currency, start_date):
        """Check for the first valid exchange rate before start_date
        and replace the Nan value at the first date."""
        days_back = 1
        while True:
            start_date_ = pd.to_datetime(start_date) - pd.Timedelta(
                days=days_back)
            end_date_ = start_date_ + pd.Timedelta(days=1)
            start_date_str = start_date_.strftime('%Y-%m-%d')
            end_date_str = end_date_.strftime('%Y-%m-%d')
            df = (web.DataReader(currency + self._base_currency + '=X',
                                 data_source='yahoo', start=start_date_str,
                                 end=end_date_str)['Adj Close'])
            if df.index[0] != start_date_:
                days_back += 1
            else:
                return df.iloc[0]

    def _update_df(self, start_date, end_date, df_to_extend):
        """ Set exchange rates for the missing dates."""
        df = self._create_dataframe(start_date, end_date)
        for currency in df_to_extend.columns:
            df = self._add_currency_to_df(currency, df, start_date, end_date)
        extended_df = pd.concat([df, df_to_extend], sort=True)
        self.start_date = start_date
        return extended_df


c = Currency()
c.set_exchange_rates('HUF', '2022-02-10')
# print(c.currencies_df)
# print(c.start_date)
c.set_exchange_rates('EUR', '2022-02-05')
print(c.currencies_df)
# print('start: ', c.start_date)
