import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class SMACross(BaseStrategy):
    def __init__(self):
        super().__init__()
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:  # check if order is pending, if so, then break out
            return

        if not self.position:
            if self.crossover > 0:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        elif self.crossover < 0:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.close(size=self.p.stake)
