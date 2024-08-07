import yfinance as yf
import numpy as np
import pandas as pd
import traceback
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator

def calculate_features_and_scale(data, tickers):

    # Calculate features
    features = []
    for ticker, hist in data.items():
        mean_price = hist['Close'].mean()
        std_dev = hist['Close'].std()
        returns = hist['Close'].pct_change().dropna()
        sharpe_ratio = returns.mean() / returns.std()
        volume = hist['Volume'].mean()
        
        # Example: Fetch additional financial metrics from yfinance (use your own method if needed)
        info = yf.Ticker(ticker).info
        eps = info.get('trailingEps', np.nan)
        pe_ratio = info.get('trailingPE', np.nan)
        market_cap = info.get('marketCap', np.nan)
        
        features.append([mean_price, std_dev, sharpe_ratio, volume, eps, pe_ratio, market_cap])

    # Create DataFrame
    feature_columns = ['Mean_Price', 'Std_Dev', 'Sharpe_Ratio', 'Volume', 'EPS', 'PE_Ratio', 'Market_Cap']
    df = pd.DataFrame(features, columns=feature_columns, index=tickers)

    # Normalize the data so that it can be used for k-means clustering
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=feature_columns, index=tickers)

    return df_scaled

def elbow_method(df):
    # Initializing an empty list to store the WCSS values
    wcss = []

    # Running k-means for a range of k values (1 to 10) and computing WCSS for each
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(df)
        wcss.append(kmeans.inertia_)

    # Plotting the WCSS against the number of clusters k
    plt.plot(range(1, 11), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

    # Using KneeLocator to find the optimal number of clusters
    kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
    optimal_k = kn.elbow

    return optimal_k

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