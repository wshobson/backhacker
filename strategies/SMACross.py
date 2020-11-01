import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class SMACross(BaseStrategy):
    params = dict(
        stake=10,
        p_fast=10,
        p_slow=30,
    )

    def __init__(self):
        super().__init__()
        sma1, sma2 = bt.ind.SMA(period=self.p.p_fast), bt.ind.SMA(period=self.p.p_slow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY" and self.crossover > 0:
            self.long(size=self.p.stake)
        if self.last_operation != "SELL" and self.crossover < 0:
            self.short(size=self.p.stake)
