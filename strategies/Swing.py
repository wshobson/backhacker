from strategies.BaseStrategy import BaseStrategy
from indicators.Swing import Swing as SwingInd


class Swing(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.indicator = SwingInd(period=14)

    def next(self):
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:  # check if order is pending, if so, then break out
            return

        # we are only interested in going long
        if not self.position:
            if self.indicator.l.signal[0] == -1:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.indicator.l.signal[0] == 1:
                self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.close(size=self.p.stake)
