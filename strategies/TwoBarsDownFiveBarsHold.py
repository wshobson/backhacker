from strategies.BaseStrategy import BaseStrategy


class TwoBarsDownFiveBarsHold(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.buyprice = None
        self.buycomm = None

    def next(self):
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:  # check if order is pending, if so, then break out
            return

        # since there is no order pending, are we in the market?
        if not self.position:  # not in the market
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                    self.order = self.buy(size=self.p.stake)
        else:  # in the market
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
