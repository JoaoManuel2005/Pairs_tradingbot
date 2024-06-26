import backtrader as bt
from src.trading_strategy import PairsTradingStrategy

def run_backtest(stock1, stock2, lookback_period=30, entry_zscore=2, exit_zscore=0.5):
    cerebro = bt.Cerebro()
    
    data1 = bt.feeds.PandasData(dataname=stock1)
    data2 = bt.feeds.PandasData(dataname=stock2)
    
    cerebro.adddata(data1)
    cerebro.adddata(data2)
    
    cerebro.addstrategy(PairsTradingStrategy, lookback_period=lookback_period, entry_zscore=entry_zscore, exit_zscore=exit_zscore)
    
    cerebro.run()
    cerebro.plot()