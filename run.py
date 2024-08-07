import yaml
from src.data_fetching import fetch_and_localize
from src.cointegration_test import perform_cointegration_test
from src.data_processing import preprocess_data, calculate_spread, calculate_zscore, elbow_method, calculate_features_and_scale
from src.backtesting import run_backtest
from src.paper_trading import AlpacaPaperTrader

from sklearn.cluster import KMeans

# Load config to access api info to then set it up
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# alpaca trading API setup
api_key = config['alpaca']['api_key']
api_secret = config['alpaca']['api_secret']
base_url = config['alpaca']['base_url']

# trading parameters
tickers = config['trading']['tickers']
lookback_period = config['trading']['lookback_period']
entry_zscore = config['trading']['entry_zscore']
exit_zscore = config['trading']['exit_zscore']
initial_cash = config['trading']['initial_cash']


# fetch historical data for all tickers
data = {}
for ticker in tickers:
    print(f"Fetching historical data for {ticker}")
    ticker_data = fetch_and_localize(ticker, '2020-01-01', '2023-01-01')
    if ticker_data is not None:
        data[ticker] = ticker_data
    else:
        print(f"Failed to fetch data for {ticker}")

# calculate the relevant features for the k-means clustering
# and scale them
df_scaled = calculate_features_and_scale(data, tickers)

#determine the optimal number of clusters using the elbow method
optimal_k = elbow_method(df_scaled)
print(f"The optimal number of clusters is: {optimal_k}")

# Apply k-means clustering
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=0)
df_scaled['Cluster'] = kmeans.fit_predict(df_scaled)


# test for cointegration between each pair inside each cluster
cointegrated_pairs = []
for cluster in df_scaled['Cluster'].unique():
    cluster_tickers = df_scaled[df_scaled['Cluster'] == cluster].index.tolist()
    for i, ticker1 in enumerate(cluster_tickers):
        for ticker2 in cluster_tickers[i+1:]:
            print(f"Testing cointegration between {ticker1} and {ticker2} in cluster {cluster}")
            if ticker1 in data and ticker2 in data:
                p_value = perform_cointegration_test(data[ticker1], data[ticker2])
                print(f"Cointegration test p-value for {ticker1} and {ticker2}: {p_value}")
                if p_value < 0.05:
                    print('Pair is cointegrated')
                    cointegrated_pairs.append((ticker1, ticker2))
                else:
                    print('Pair is not cointegrated')
        
# backtest each cointegrated pairs
for ticker1, ticker2 in cointegrated_pairs:
    print(f"Backtesting strategy for pair: {ticker1} and {ticker2}")
    stock1 = data[ticker1]
    stock2 = data[ticker2]

    # preprocess data and calculate spread and z-score of each cointegrated pair
    data = preprocess_data(stock1, stock2)
    spread = calculate_spread(stock1, stock2)['spread']
    zscore = calculate_zscore(spread, lookback_period)

    # backtest the strategy
    run_backtest(stock1, stock2, lookback_period, entry_zscore, exit_zscore)

        # # Example paper trading usage
        # print("Setting up paper trading")
        # trader = AlpacaPaperTrader(config_path='config/config.yaml')
        # account_info = trader.get_account_info()
        # print(account_info)
        
        # # Place an order (for demonstration purposes)
        # print("Placing an order")
        # order = trader.place_order(symbol=pairs[0], qty=1, side='buy')
        # print(order)