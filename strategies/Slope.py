import backtrader as bt
from config import ENV, PRODUCTION
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
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.ma1 > self.ma1[-1]:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.ma1 < self.ma1[-1]:
                self.short(size=self.p.stake)
