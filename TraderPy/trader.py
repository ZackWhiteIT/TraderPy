from groupme import groupme
import gdax
import pandas as pd
import pandas_datareader as web
import datetime


class trader:

    def __init__(self):
        self.message_bot = groupme()
        self.client = gdax.PublicClient()

    def log(self, level, message):
        print('{} {} {}'.format(datetime.datetime.now().isoformat(),
                                level, message))

    def get_ticker(self, asset):
        self.log('I', 'Getting ticker information for {}'.format(asset))
        try:
            ticker = self.client.get_product_ticker(asset)
            self.log(
                'I', 'Ticker information for {} successfully retrieved'.format(
                    asset))
        except Exception as e:
            self.log('E', str(e))
        return ticker

    def get_macd(self, ticker):
        ''' MACD: (12-day Exponential Moving Average (EMA) - 26-day EMA) '''
        self.log('I', 'Calculating MACD for {}'.format(ticker))
        self.log('I', 'Getting historical info for {}'.format(
            ticker))

        # Calculate dates for calculations
        end = datetime.datetime.now() - datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=365)

        history = None

        try:
            # Submit the request to Yahoo Finance's API
            history = web.get_data_yahoo(ticker, start, end)
            self.log(
                'I', 'Historical info for {} successfully retrieved'.format(
                    ticker))
        except Exception as e:
            self.log('E', str(e))

        # Calculate 30-day Moving Average (MAVG)
        # Only get the next-to-last column (Adj Close MAVG)
        # TODO: Re-write this to only calculate the rolling mean on Adj Close
        # rather than all columns
        mavg = history.rolling(center=False, window=30).mean().iloc[:, -2]

        # Calculate 26-day Exponential Moving Average (EMA)
        # Only get the next-to-last column (Adj Close MAVG)
        # TODO: Re-write this to only calculate the rolling mean on Adj Close
        # rather than all columns
        ema_twenty_six = history.ewm(adjust=True,span=26,ignore_na=False,min_periods=0).mean().iloc[:, -2]

        # Calculate 12-day Exponential Moving Average (EMA)
        # Only get the next-to-last column (Adj Close MAVG)
        # TODO: Re-write this to only calculate the rolling mean on Adj Close
        # rather than all columns
        ema_twelve = history.ewm(adjust=True,span=12,ignore_na=False,min_periods=0).mean().iloc[:, -2]

        # Calculate Moving Average Convergence Divergence (MACD)
        # Only get the next-to-last column (Adj Close MAVG)
        macd = ema_twelve - ema_twenty_six

        # Add MACD to history data frame
        history = history.assign(MACD=macd.values)

        return history
