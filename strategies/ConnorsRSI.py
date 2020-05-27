from config import ENV, PRODUCTION
from indicators.ConnorsRSI import ConnorsRSI as ConnorsRSIInd
from strategies.BaseStrategy import BaseStrategy


class ConnorsRSI(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.indicator = ConnorsRSIInd()

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:  # waiting for live status in production
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.indicator.crsi[0] <= 10:
                self.long(size=self.p.stake)

        if self.last_operation != "SELL":
            if self.indicator.crsi[0] >= 90:
                self.short(size=self.p.stake)
