from groupme import groupme
import cbpro
import pandas as pd
import pandas_datareader as web
import datetime
import numpy as np


class trader:
    def __init__(self):
        self.message_bot = groupme()
        self.client = cbpro.PublicClient()
        self.ticker_cache = None
        self.history_cache = None

    def log(self, level, message):
        print("{} {} {}".format(datetime.datetime.now().isoformat(), level, message))

    def get_ticker(self, ticker):
        self.log("I", "Getting ticker information for {}".format(ticker))
        try:
            self.ticker_cache = self.client.get_product_ticker(ticker)
            self.log(
                "I", "Ticker information for {} successfully retrieved".format(ticker)
            )
        except Exception as e:
            self.log("E", str(e))

        return self.ticker_cache

    def get_history(self, ticker):
        self.log("I", "Getting historical info for {}".format(ticker))

        # Calculate dates for calculations
        end = datetime.datetime.now() - datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=365)

        history = None

        try:
            # Submit the request to Yahoo Finance's API
            history = web.get_data_yahoo(ticker, start, end)
            self.log(
                "I", "Historical info for {} successfully retrieved".format(ticker)
            )
        except Exception as e:
            self.log("E", str(e))

        self.history_cache = history

        return history

    def get_macd(self, ticker):
        """ MACD: (12-day Exponential Moving Average (EMA) - 26-day EMA) """
        self.log("I", "Calculating MACD for {}".format(ticker))

        if self.ticker_cache != ticker:
            self.ticker_cache = ticker
            self.history_cache = None

        if self.history_cache is None:
            self.get_history(ticker)

        # Calculate 30-day Moving Average (MAVG)
        # Only get the next-to-last column (Adj Close MAVG)
        # TODO: Re-write this to only calculate the rolling mean on Adj Close
        # rather than all columns
        mavg = self.history_cache.rolling(center=False, window=30).mean().iloc[:, -2]

        # Calculate 26-day Exponential Moving Average (EMA)
        # Only get the next-to-last column (Adj Close MAVG)
        # TODO: Re-write this to only calculate the rolling mean on Adj Close
        # rather than all columns
        ema_twenty_six = (
            self.history_cache.ewm(adjust=True, span=26, ignore_na=False, min_periods=0)
            .mean()
            .iloc[:, -2]
        )

        # Calculate 12-day Exponential Moving Average (EMA)
        # Only get the next-to-last column (Adj Close MAVG)
        # TODO: Re-write this to only calculate the rolling mean on Adj Close
        # rather than all columns
        ema_twelve = (
            self.history_cache.ewm(adjust=True, span=12, ignore_na=False, min_periods=0)
            .mean()
            .iloc[:, -2]
        )

        # Calculate Moving Average Convergence Divergence (MACD)
        # Only get the next-to-last column (Adj Close MAVG)
        macd = ema_twelve - ema_twenty_six

        # Add MACD to history data frame
        self.history_cache = self.history_cache.assign(MACD=macd.values)

        return macd

    def get_rsi(self, ticker):
        """
        Relative Strength Index (RSI)
        RSI = 100 - 100 / (1 + RS)
        RS = Average gain of last 14 trading days / Average loss
             of last 14 trading days
        """
        if self.ticker_cache != ticker:
            self.ticker_cache = ticker
            self.history_cache = None

        if self.history_cache is None:
            self.get_history(ticker)

        series = self.history_cache["Adj Close"]
        print(series)
        period = 14  # 14 days for Relative Strength Index

        # Calculate RSI
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        # first value is sum of avg gains
        u[u.index[period - 1]] = np.mean(u[:period])
        u = u.drop(u.index[: (period - 1)])
        # first value is sum of avg losses
        d[d.index[period - 1]] = np.mean(d[:period])
        d = d.drop(d.index[: (period - 1)])
        rs = pd.stats.moments.ewma(
            u, com=period - 1, adjust=False
        ) / pd.stats.moments.ewma(d, com=period - 1, adjust=False)
        rsi = 100 - 100 / (1 + rs)

        # Add RSI to history data frame
        self.history_cache = self.history_cache.assign(RSI=rsi.values)

        return rsi
