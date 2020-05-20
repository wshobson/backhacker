import backtrader as bt
from indicators.DonchianChannels import DonchianChannels


class DonchianHiLow(bt.Strategy):
    def __init__(self):
        self.indicator = DonchianChannels()

    def next(self):
        if self.data[0] > self.indicator.dch[0]:
            self.buy()
        elif self.data[0] < self.indicator.dcl[0]:
            self.sell()
