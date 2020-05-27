from strategies.BaseStrategy import BaseStrategy
from config import ENV, PRODUCTION
from indicators.Extrema import Extrema as ExtremaInd


class Extrema(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.indicator = ExtremaInd()

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.indicator.l.lmin[0] > self.data[0]:
            self.long(size=self.p.stake)
        elif self.indicator.l.lmax[0] < self.data[0]:
            self.short(size=self.p.stake)
