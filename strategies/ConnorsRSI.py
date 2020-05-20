import backtrader as bt
from indicators.ConnorsRSI import ConnorsRSI as ConnorsRSIInd


class ConnorsRSI(bt.Strategy):
    def __init__(self):
        self.indicator = ConnorsRSIInd()

    def next(self):
        if self.indicator.crsi[0] <= 10:
            self.buy()
        elif self.indicator.crsi[0] >= 90:
            self.sell()
