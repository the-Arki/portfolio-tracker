import pandas as pd
from pandas_datareader import data as web
from datetime import datetime


class Currency:
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
            (the last date has to be today)
    """
    _base_currency = 'USD'
    start_date = None
    today = datetime.date(datetime.now())
    try:
        currencies_df = pd.read_csv('files/exchange_rates.csv',
                                    parse_dates=True, index_col=[0])
        start_date = currencies_df.index[0].strftime("%Y-%m-%d")
    except (pd.errors.EmptyDataError, FileNotFoundError):
        currencies_df = pd.DataFrame()

    @classmethod
    def _change_df_in_class(cls, df):
        cls.currencies_df = df
        return cls.currencies_df

    @classmethod
    def _set_start_date(cls, start):
        print(start)
        print(type(start))
        cls.start_date = start

    @classmethod
    def _check_currency(cls, currency):
        """Check if currency is in the exchange rates database and
        return a boolean"""
        if cls.currencies_df.empty:
            return False
        elif currency not in cls.currencies_df.columns:
            return False
        else:
            return True

    @classmethod
    def _create_dataframe(cls, start_date, end_date):
        "create a dataframe for exchange rates if it is not existing yet."
        start_date = start_date
        end_date = end_date
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        df = pd.DataFrame(index=dates)
        return df

    @classmethod
    def set_exchange_rates(cls, currency, start_date):
        """Set the exchange range for the passed currency.
        If the given start date is earlier than the current cls.start_date,
        then update all values with this new start.
        """
        df_changed = False
        df = cls.currencies_df.copy()
        if not cls.start_date:
            cls._set_start_date(start_date)
        if cls.currencies_df.empty:
            df = cls._create_dataframe(cls.start_date, cls.today)
        if not cls._check_currency(currency):
            df = (cls._add_currency_to_df(currency, df,
                                          cls.start_date, cls.today))
            df_changed = True
        if start_date < cls.start_date:
            end_date = pd.to_datetime(cls.start_date) - pd.Timedelta(days=1)
            df = cls.update_df(start_date, end_date, df)
            df_changed = True
        if df_changed:
            cls._change_df_in_class(df)
            cls.save_df(df)
        return df

    @classmethod
    def save_df(cls, df):
        print('df before saving: \n', df)
        df.to_csv('files/exchange_rates.csv')

    @classmethod
    def _add_currency_to_df(cls, currency, df, start_date, end_date):
        """Add the currency to the exchange rates database.
        If the first value is NaN, then look for an earlier value to start.
        """
        df_ = df.copy()
        if currency == cls._base_currency:
            df_[currency] = 1
            return df_
        start_date_ = datetime.strptime(start_date, '%Y-%m-%d').date()
        attempt = 0
        while attempt < 10:
            try:
                data = (web.DataReader(currency + cls._base_currency + '=X',
                                       data_source='yahoo', start=start_date_,
                                       end=end_date)['Adj Close'])
                break
            except KeyError:
                start_date_ = start_date_ - pd.Timedelta(days=1)
                attempt += 1
        data = data[~data.index.duplicated(keep='first')]
        df_[currency] = data
        if pd.isna(df_.loc[start_date, currency]):
            df_.loc[start_date, currency] = (
                cls._get_first_value(currency, start_date))
        df_[currency].ffill(inplace=True)
        return df_

    @classmethod
    def _get_first_value(cls, currency, start_date):
        """Check for the first valid exchange rate before start_date
        and replace the Nan value at the first date."""
        days_back = 1
        while True:
            start_date_ = pd.to_datetime(start_date) - pd.Timedelta(
                days=days_back)
            end_date_ = start_date_ + pd.Timedelta(days=1)
            start_date_str = start_date_.strftime('%Y-%m-%d')
            end_date_str = end_date_.strftime('%Y-%m-%d')
            df = (web.DataReader(currency + cls._base_currency + '=X',
                                 data_source='yahoo', start=start_date_str,
                                 end=end_date_str)['Adj Close'])
            if df.index[0] != start_date_:
                days_back += 1
            else:
                return df.iloc[0]

    @classmethod
    def update_df(cls, start_date, end_date, df_to_extend):
        """ Set exchange rates for the missing dates."""
        end_date = end_date
        df = cls._create_dataframe(start_date, end_date)
        for currency in df_to_extend.columns:
            df = cls._add_currency_to_df(currency, df, start_date, end_date)
        extended_df = pd.concat([df, df_to_extend], sort=True)
        cls._set_start_date(start_date)
        return extended_df


# -------------------------------------------------------------
if __name__ == "__main__":
    c = Currency
    c.set_exchange_rates('HUF', '2022-03-13')
    # print(c.currencies_df)
    # print(c.start_date)
    # c.set_exchange_rates('EUR', '2022-02-05')
    # print(c.currencies_df)
    # print('start: ', c.start_date)
