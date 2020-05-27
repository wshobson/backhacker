import backtrader as bt
from config import ENV, PRODUCTION
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
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.rsi > self.rsi[-1] and self.rsi > self.p.oversold:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.rsi < self.rsi[-1] and self.rsi < self.p.overbought:
                self.short(size=self.p.stake)
