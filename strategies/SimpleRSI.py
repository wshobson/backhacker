import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class SimpleRSI(BaseStrategy):
    params = dict(
        period_ema_fast=10,
        period_ema_slow=100
    )

    def __init__(self):
        super().__init__()
        self.ema_fast = bt.ind.EMA(period=self.p.period_ema_fast)
        self.ema_slow = bt.ind.EMA(period=self.p.period_ema_slow)
        self.rsi = bt.ind.RSI()

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:  # waiting for live status in production
            return

        if self.order:
            return

        # stop Loss
        if self.profit < -0.03:
            self.log("STOP LOSS: percentage %.3f %%" % self.profit)
            self.short()

        if self.last_operation != "BUY":
            if self.rsi < 30 and self.ema_fast > self.ema_slow:
                self.long()

        if self.last_operation != "SELL":
            if self.rsi > 70:
                self.short()
