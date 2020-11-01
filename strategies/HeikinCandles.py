import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class HeikinCandles(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.HA = bt.indicators.HeikinAshi(self.datas[0])

    def next(self):
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.HA.ha_close[0] > self.HA.ha_open[0] and self.HA.ha_close[-1] < self.HA.ha_open[-1]:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.HA.ha_close[0] < self.HA.ha_open[0]:
                self.short(size=self.p.stake)
