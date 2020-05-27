import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class MultipleSMACross(BaseStrategy):
    def __init__(self):
        super().__init__()
        sma1 = bt.ind.SMA(self.data0, period=10)
        sma2 = bt.ind.SMA(self.data0, period=30)
        self.crossover0 = bt.ind.CrossOver(sma1, sma2)

        sma1 = bt.ind.SMA(self.data1, period=10)
        sma2 = bt.ind.SMA(self.data1, period=30)
        self.crossover1 = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if not self.getposition(self.data0).size and self.crossover0 > 0:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(data=self.data0, size=self.p.stake)  # enter long

        if not self.getposition(self.data1).size and self.crossover1 > 0:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(data=self.data1, size=self.p.stake)  # enter long

        # in the market & cross to the downside
        if self.getposition(self.data0).size and self.crossover0 <= 0:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.close(data=self.data0, size=self.p.stake)  # close long position
        # in the market & cross to the downside
        if self.getposition(self.data1).size and self.crossover1 <= 0:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.close(data=self.data1, size=self.p.stake)  # close long position
