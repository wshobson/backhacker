import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class ExtendedCross(BaseStrategy):
    params = dict(
        stake=10,
        ma1=5,
        ma2=20,
        ma3=50,
        atr=1,
    )

    def __init__(self):
        super().__init__()
        self.ma1 = bt.ind.EMA(self.datas[0], period=self.p.ma1)
        self.ma2 = bt.ind.EMA(self.datas[0], period=self.p.ma2)
        self.ma3 = bt.ind.EMA(self.datas[0], period=self.p.ma3)
        self.atr = bt.ind.ATR(self.datas[0])

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.ma1 > (self.ma2 + self.p.atr * self.atr) and self.dataclose[0] > self.ma3:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.ma1 < (self.ma2 - self.p.atr * self.atr) and self.dataclose[0] < self.ma3:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
