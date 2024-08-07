# Pairs Trading Bot

## Overview

Pairs Trading Bot is a Python-based algorithmic trading bot that implements a pairs trading strategy. The bot uses historical stock data to identify pairs of stocks that are cointegrated and executes trades based on statistical arbitrage.

### How the Algorithm Works

1. **Data Fetching**: The bot fetches historical stock data using the `yfinance` library. This data includes daily prices for a specified date range.
2. **K-means clustering**: The securities are put into clusters based on their performance and features
3. **Cointegration Test**: The bot tests pairs of stocks within each cluster for cointegration using the Augmented Dickey-Fuller (ADF) test. Cointegration indicates that two stocks move together over time, which is essential for pairs trading.
4. **Spread Calculation**: For each pair of cointegrated stocks, the bot calculates the spread, which is the difference between the prices of the two stocks.
5. **Z-score Calculation**: The bot calculates the z-score of the spread. The z-score indicates how many standard deviations the spread is from its mean. This helps in identifying trading signals.
6. **Trading Signals**: The bot generates trading signals based on the z-score:
   - **Entry Signal**: When the z-score exceeds a certain threshold, it indicates that the spread is wide, and a mean reversion trade is initiated. The bot goes long on the underperforming stock and short on the outperforming stock.
   - **Exit Signal**: When the z-score reverts to zero or crosses another threshold, it indicates that the spread has reverted to the mean, and the trade is closed.
7. **Backtesting**: The bot backtests the trading strategy using historical data to evaluate its performance.
8. **Paper Trading**: The bot can execute paper trades using the Alpaca API, which allows for simulated trading without real money.

## Features

- Fetch historical stock data using `yfinance`
- Clustering of securities
- Test for cointegration between pairs of stocks
- Calculate spread and z-score for pairs trading
- Backtest trading strategy
- Paper trading using Alpaca API