from strategies.BaseStrategy import BaseStrategy
from config import ENV, PRODUCTION
from indicators.KeltnerChannel import KeltnerChannel as KeltnerChannelInd


class KeltnerChannel(BaseStrategy):
    params = dict(
        stake=10,
    )

    def __init__(self):
        super().__init__()
        self.indicator = KeltnerChannelInd()

    def next(self):
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.indicator.l.lower[0] > self.data[0]:
            self.long(size=self.p.stake)
        elif self.indicator.l.upper[0] < self.data[0]:
            self.short(size=self.p.stake)
