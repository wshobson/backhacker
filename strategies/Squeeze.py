from strategies.BaseStrategy import BaseStrategy
from config import ENV, PRODUCTION
from indicators.Squeeze import Squeeze as SqueezeInd


class Squeeze(BaseStrategy):
    params = dict(
        stake=10
    )

    def __init__(self):
        super().__init__()
        self.indicator = SqueezeInd()

    def next(self):
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        # TODO
        # if self.indicator.l.exited:
