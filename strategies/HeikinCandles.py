import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class HeikinCandles(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.HA = bt.indicators.HeikinAshi(self.datas[0])

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.HA.ha_close[0] > self.HA.ha_open[0] and self.HA.ha_close[-1] < self.HA.ha_open[-1]:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.HA.ha_close[0] < self.HA.ha_open[0]:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
