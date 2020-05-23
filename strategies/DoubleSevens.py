import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class DoubleSevens(BaseStrategy):
    """
    Implementation of the Double 7's strategy from Larry Connor's
    Short-Term Strategies book, Chapter 10
    """
    def __init__(self):
        super().__init__()
        self.sma200 = bt.ind.SMA(self.datas[0], period=200)
        self.high_bar = bt.ind.Highest(self.data.high, period=7)
        self.low_bar = bt.ind.Lowest(self.data.low, period=7)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.sma200[0] < self.dataclose[0] <= self.low_bar[0]:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.dataclose[0] >= self.high_bar[0]:
                self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
