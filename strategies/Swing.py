from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy
from indicators.Swing import Swing as SwingInd


class Swing(BaseStrategy):
    params = dict(
        stake=100,
        period=7,
    )

    def __init__(self):
        super().__init__()
        self.indicator = SwingInd(period=self.p.period)

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.indicator.l.signal[0] == -1:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.indicator.l.signal[0] == 1:
                self.short(size=self.p.stake)
