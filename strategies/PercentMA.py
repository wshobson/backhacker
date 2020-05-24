import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class PercentMA(BaseStrategy):
    params = dict(
        stake=10,
        percent_period=200,
        macd_limit1=10,
        macd_limit2=30,
        period1=12,
        period2=26,
    )

    def __init__(self):
        super().__init__()
        self.ma1 = bt.ind.EMA(self.datas[0], period=self.p.period1)
        self.ma2 = bt.ind.EMA(self.datas[0], period=self.p.period2)
        self.diff = self.ma1 - self.ma2
        self.prank_diff = bt.ind.PercentRank(self.diff, period=self.p.percent_period) * 100

        self.buy_limit_macd1 = self.p.macd_limit1
        self.sell_limit_macd1 = 100 - self.buy_limit_macd1

        self.buy_limit_macd2 = self.p.macd_limit2
        self.sell_limit_macd2 = 100 - self.buy_limit_macd2

        self.pending_buy = False
        self.pending_sell = False

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.prank_diff <= self.buy_limit_macd1:
                self.pending_buy = True
            elif self.pending_buy == True and self.prank_diff >= self.buy_limit_macd2:
                self.pending_buy = False
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.prank_diff >= self.sell_limit_macd1:
                self.pending_sell = True
            elif self.pending_sell == True and self.prank_diff <= self.sell_limit_macd2:
                self.pending_sell = False
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
