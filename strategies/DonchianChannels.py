from strategies.BaseStrategy import BaseStrategy
from indicators.DonchianChannels import DonchianChannels as DonchianChannelsInd


class DonchianChannels(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.indicator = DonchianChannelsInd()

    def next(self):
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:  # check if order is pending, if so, then break out
            return

        if self.data[0] > self.indicator.dch[0]:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(size=self.p.stake)
        elif self.data[0] < self.indicator.dcl[0]:
            self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.sell(size=self.p.stake)
