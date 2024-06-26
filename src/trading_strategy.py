import backtrader as bt

class PairsTradingStrategy(bt.Strategy):
    params = (
        ('lookback_period', 30),
        ('entry_zscore', 2),
        ('exit_zscore', 0.5),
    )

    def __init__(self):
        self.data1 = self.datas[0]
        self.data2 = self.datas[1]
        
        self.spread = self.data1.close - self.data2.close
        self.mean = bt.indicators.SimpleMovingAverage(self.spread, period=self.params.lookback_period)
        self.zscore = (self.spread - self.mean) / bt.indicators.StandardDeviation(self.spread, period=self.params.lookback_period)

    def next(self):
        if self.zscore > self.params.entry_zscore:
            self.sell(data=self.data1)
            self.buy(data=self.data2)
        elif self.zscore < -self.params.entry_zscore:
            self.buy(data=self.data1)
            self.sell(data=self.data2)
        
        if self.position:
            if self.zscore < self.params.exit_zscore and self.zscore > -self.params.exit_zscore:
                self.close(data=self.data1)
                self.close(data=self.data2)