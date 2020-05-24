import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class RSICross(BaseStrategy):
    params = dict(
        stake=10,
        ma1=14,
        ma2=30,
        period=6,
        gamma=0.5,
        lower_limit=0.2,
        upper_limit=0.8
    )

    def __init__(self):
        super().__init__()
        self.ma1 = bt.ind.SMA(self.datas[0], period=self.p.ma1)
        self.ma2 = bt.ind.SMA(self.datas[0], period=self.p.ma2)
        self.rsi = bt.ind.LaguerreRSI(self.datas[0], period=self.p.period, gamma=self.p.gamma)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.ma1 > self.ma2 and self.rsi > self.rsi[-1] and self.rsi > self.p.lower_limit:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.ma1 < self.ma2 and self.rsi < self.rsi[-1] and self.rsi < self.p.upper_limit:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
