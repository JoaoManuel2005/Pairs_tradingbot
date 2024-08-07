import yfinance as yf
import numpy as np
import pandas as pd
import traceback



def fetch_and_localize2(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, threads=False)
        if not data.empty:
            if not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data.index)
            if data.index.tz is None:
                data.index = pd.DatetimeIndex(data.index).tz_localize('UTC')
            else:
                data.index = pd.DatetimeIndex(data.index).tz_convert('UTC')
        return data
    except Exception as e:
        print(f"Error localizing timezone:")
        print(traceback.format_exc())


def fetch_and_localize(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, threads=False)
        data.index = pd.to_datetime(data.index)
        # Ensure the index is timezone-aware
        if data.index.tz is None:
            data.index = data.index.tz_localize('UTC', ambiguous='infer', nonexistent='shift_forward')
        else:
            data.index = data.index.tz_convert('UTC')
        return data
    except Exception as e:
        print(f"Error localizing timezone:")
        print(traceback.format_exc())


def fetch_realtime_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            if data.index.tz is None:
                data.index = data.index.tz_localize('UTC')
            else:
                data.index = data.index.tz_convert('UTC')
        return data
    except Exception as e:
        print(f"Error localizing timezone: {e}")        


def fetch_data_for_features(tickers):
    # Fetch data for each ticker
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='5y')
        data[ticker] = hist
    
    return data