import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class StochasticCross(BaseStrategy):
    params = dict(
        stake=10,
        ma1=14,
        ma2=30,
        period=14,
    )

    def __init__(self):
        super().__init__()
        self.ma1 = bt.ind.SMA(self.datas[0], period=self.p.ma1)
        self.ma2 = bt.ind.SMA(self.datas[0], period=self.p.ma2)
        self.stoch = bt.ind.Stochastic(self.datas[0], period=self.p.period)

    def next(self):
        self.update_profit()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.ma1 > self.ma2 and self.stoch < 20:
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.ma1 < self.ma2 and self.stoch > 80:
                self.short(size=self.p.stake)
