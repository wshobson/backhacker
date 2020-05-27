import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class GoldenCross(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.sma50 = bt.ind.SMA(self.datas[0], period=50)
        self.sma200 = bt.ind.SMA(self.datas[0], period=200)

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.sma50[0] > self.sma200[0] and self.sma50[-1] <= self.sma200[-1]:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.sma50[0] < self.sma200[0] and self.sma50[-1] >= self.sma200[-1]:
                self.short(size=self.p.stake)
