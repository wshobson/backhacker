import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class Slope(BaseStrategy):
    params = dict(
        stake=10,
        ma1_period=14,
    )

    def __init__(self):
        super().__init__()
        self.ma1 = bt.ind.SMA(self.datas[0], period=self.p.ma1_period)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.ma1 > self.ma1[-1]:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.ma1 < self.ma1[-1]:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
