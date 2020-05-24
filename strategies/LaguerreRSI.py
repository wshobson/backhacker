import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class LaguerreRSI(BaseStrategy):
    params = dict(
        stake=10,
        period=6,
        gamma=0.5,
        overbought=0.8,
        oversold=0.2,
    )

    def __init__(self):
        super().__init__()
        self.rsi = bt.ind.LaguerreRSI(self.datas[0], period=self.p.period, gamma=self.p.gamma)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.rsi > self.rsi[-1] and self.rsi > self.p.oversold:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.rsi < self.rsi[-1] and self.rsi < self.p.overbought:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
