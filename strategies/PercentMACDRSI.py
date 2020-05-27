import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy


class PercentMACDRSI(BaseStrategy):
    params = dict(
        stake=10,
        rsi_period=14,
        percent_period=200,
        rsi_limit1=10,
        rsi_limit2=30,
        macd_limit1=10,
        macd_limit2=30,
        period1=12,
        period2=26,
    )

    def __init__(self):
        super().__init__()
        self.rsi = bt.ind.RSI(self.datas[0], period=self.p.rsi_period)
        self.prank_rsi = bt.ind.PercentRank(self.rsi, period=self.p.percent_period) * 100
        self.macd = bt.ind.MACD(self.datas[0], period_me1=self.p.period1, period_me2=self.p.period2)
        self.prank_macd = bt.ind.PercentRank(self.macd, period=self.p.percent_period) * 100

        self.buy_limit_rsi1 = self.p.rsi_limit1
        self.sell_limit_rsi1 = 100 - self.buy_limit_rsi1

        self.buy_limit_rsi2 = self.p.rsi_limit2
        self.sell_limit_rsi2 = 100 - self.buy_limit_rsi2

        self.buy_limit_macd1 = self.p.macd_limit1
        self.sell_limit_macd1 = 100 - self.buy_limit_macd1

        self.buy_limit_macd2 = self.p.macd_limit2
        self.sell_limit_macd2 = 100 - self.buy_limit_macd2

        self.pending_buy = False
        self.pending_sell = False

    def next(self):
        self.update_indicators()
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.status != "LIVE" and ENV == PRODUCTION:
            return

        if self.order:
            return

        if self.last_operation != "BUY":
            if self.prank_rsi <= self.buy_limit_rsi1 and self.prank_macd <= self.buy_limit_macd1:
                self.pending_buy = True
            elif self.pending_buy == True and self.prank_rsi >= self.buy_limit_rsi2 and self.prank_macd >= self.buy_limit_macd2:
                self.pending_buy = False
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.prank_rsi >= self.sell_limit_rsi1 and self.prank_macd >= self.sell_limit_macd1:
                self.pending_sell = True
            elif self.pending_sell == True and self.prank_rsi <= self.sell_limit_rsi2 and self.prank_macd <= self.sell_limit_macd2:
                self.pending_sell = False
                self.short(size=self.p.stake)
