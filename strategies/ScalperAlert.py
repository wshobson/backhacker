from strategies.BaseStrategy import BaseStrategy
from indicators.ScalperAlert import ScalperAlert


class ScalperStrategy(BaseStrategy):
    params = dict(
        stake=10
    )

    def __init__(self):
        super().__init__()
        self.indicator = ScalperAlert()

    def next(self):
        self.broker.getcash()
        if self.indicator.l.signal[0] > 0:
            self.long(size=self.p.stake, reverse=True, stop=self.indicator.l.stop[0])
            return
        if self.indicator.l.signal[0] < 0:
            self.short(size=self.p.stake, reverse=True, stop=self.indicator.l.stop[0])
