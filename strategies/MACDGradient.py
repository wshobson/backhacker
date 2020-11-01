import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class MACDGradient(BaseStrategy):
    params = dict(
        stake=10,
        period_me1=12,
        period_me2=26,
    )

    def __init__(self):
        super().__init__()
        self.MACD = bt.ind.MACD(self.data.close, period_me1=self.p.period_me1, period_me2=self.p.period_me2)

    def next(self):
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.MACD[0] > self.MACD[-1] > self.MACD[-2]:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.MACD[0] < self.MACD[-1] < self.MACD[-2]:
                self.short(size=self.p.stake)
