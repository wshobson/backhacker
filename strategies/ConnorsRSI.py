from strategies.BaseStrategy import BaseStrategy
from indicators.ConnorsRSI import ConnorsRSI as ConnorsRSIInd


class ConnorsRSI(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.indicator = ConnorsRSIInd()

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if self.indicator.crsi[0] <= 10:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(size=self.p.stake)
        elif self.indicator.crsi[0] >= 90:
            self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.sell(size=self.p.stake)
