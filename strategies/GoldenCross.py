import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class GoldenCross(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.sma50 = bt.ind.SMA(self.datas[0], period=50)
        self.sma200 = bt.ind.SMA(self.datas[0], period=200)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.sma50[0] > self.sma200[0] and self.sma50[-1] <= self.sma200[-1]:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.sma50[0] < self.sma200[0] and self.sma50[-1] >= self.sma200[-1]:
                self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.close(size=self.p.stake)
