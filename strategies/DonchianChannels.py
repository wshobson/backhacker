from config import ENV, PRODUCTION
from indicators.DonchianChannels import DonchianChannels as DonchianChannelsInd
from strategies.BaseStrategy import BaseStrategy


class DonchianChannels(BaseStrategy):
    params = dict(
        stake=10,

    )

    def __init__(self):
        super().__init__()
        self.indicator = DonchianChannelsInd()

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:  # waiting for live status in production
            return

        if self.order:
            return

        if self.data[0] > self.indicator.dch[0]:
            self.long(size=self.p.stake)
        elif self.data[0] < self.indicator.dcl[0]:
            self.short(size=self.p.stake)
