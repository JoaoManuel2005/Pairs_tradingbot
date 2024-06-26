import pandas as pd
import numpy as np

def preprocess_data(stock1, stock2):
    # Ensure both dataframes have the same index
    data = pd.DataFrame({'stock1': stock1['Close'], 'stock2': stock2['Close']})
    
    # Drop any rows with NaN values
    data.dropna(inplace=True)
    
    return data

def calculate_spread(stock1, stock2):
    data = preprocess_data(stock1, stock2)
    data['spread'] = data['stock1'] - data['stock2']
    return data

def calculate_zscore(spread, lookback_period):
    spread_mean = spread.rolling(window=lookback_period).mean()
    spread_std = spread.rolling(window=lookback_period).std()
    zscore = (spread - spread_mean) / spread_std
    return zscore