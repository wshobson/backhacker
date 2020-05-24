import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class SimpleRSI(BaseStrategy):
    params = dict(
        stake=10,
        period=14,
        buy_limit=60,
        sell_limit=40,
    )

    def __init__(self):
        super().__init__()
        self.rsi = bt.ind.RSI(self.data.close, period=self.p.period)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        # we only care about going long
        if not self.position:
            if self.rsi > self.p.buy_limit:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.rsi < self.p.sell_limit:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
