from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class TwoBarsDownFiveBarsHold(BaseStrategy):
    params = dict(
        stake=10,
    )

    def __init__(self):
        super().__init__()

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if len(self) >= (self.bar_executed + 5):
                self.short(size=self.p.stake)
