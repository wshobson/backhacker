import backtrader as bt

from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class BollingerBands(BaseStrategy):
    params = dict(
        stake=10,
        bbands_period=20,
    )

    def __init__(self):
        super().__init__()

        self.redline = None
        self.blueline = None

        self.bband = bt.indicators.BBands(self.datas[0], period=self.p.bbands_period)

    def next(self):
        self.update_indicators()
        self.log('Close, %.2f' % self.dataclose[0])

        if self.status != "LIVE" and ENV == PRODUCTION:  # waiting for live status in production
            return

        if self.order:
            return

        if self.dataclose < self.bband.l.bot and self.last_operation != "BUY":
            self.redline = True

        if self.dataclose > self.bband.l.top and self.last_operation != "SELL":
            self.blueline = True

        if self.dataclose > self.bband.l.mid and self.last_operation != "BUY" and self.redline:
            self.long(size=self.p.stake)

        if self.dataclose > self.bband.l.top and self.last_operation != "BUY":
            self.long(size=self.p.stake)

        if self.dataclose < self.bband.l.mid and self.last_operation != "SELL" and self.blueline:
            self.blueline = False
            self.redline = False
            self.short(size=self.p.stake)
