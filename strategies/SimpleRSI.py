import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class SimpleRSI(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def next(self):
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:  # check if order is pending, if so, then break out
            return

        if not self.position:
            if self.rsi < 30:
                self.buy(size=self.p.stake)
        else:
            if self.rsi > 70:
                self.sell(size=self.p.stake)
