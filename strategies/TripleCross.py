import backtrader as bt
from config import ENV, PRODUCTION
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
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.ma1 > self.ma2 > self.ma3:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.ma1 < self.ma2 < self.ma3:
                self.short(size=self.p.stake)
