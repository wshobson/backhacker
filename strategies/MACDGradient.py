import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class MACDGradient(BaseStrategy):
    params = dict(
        stake=10,
        period_me1=12,
        period_me2=26,
    )

    def __init__(self):
        super().__init__()
        self.MACD = bt.ind.MACD(self.data.close, period_me1=self.p.period_me1, period_me2=self.p.period_me2)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.MACD[0] > self.MACD[-1] > self.MACD[-2]:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.MACD[0] < self.MACD[-1] < self.MACD[-2]:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
