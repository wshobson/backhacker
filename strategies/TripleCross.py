import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class TripleCross(BaseStrategy):
    params = dict(
        stake=10,
        ma1_period=5,
        ma2_period=8,
        ma3_period=11,
    )

    def __init__(self):
        super().__init__()
        self.ma1 = bt.ind.SMA(self.datas[0], period=self.p.ma1_period)
        self.ma2 = bt.ind.SMA(self.datas[0], period=self.p.ma2_period)
        self.ma3 = bt.ind.SMA(self.datas[0], period=self.p.ma3_period)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.ma1 > self.ma2 > self.ma3:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.ma1 < self.ma2 < self.ma3:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
