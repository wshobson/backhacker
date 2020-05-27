import backtrader as bt
from config import ENV, PRODUCTION
from strategies.BaseStrategy import BaseStrategy
from indicators.Laguerre import Laguerre
from indicators.VIXFix import VIXFix


class LaguerreWilliams(BaseStrategy):
    params = dict(
        stake=10,
        short_gamma=0.4,
        long_gamma=0.8,
        pctile=90,
        wrnpctile=70,
        lkbT=200,
        lkbB=200,
        pd=22,  # LookBack Period Standard Deviation High
        bbl=20,  # Bollinger Band Length
        mult=2,  # Bollinger Band Standard Deviation Up
        lb=50,
        ph=0.85,
        pl=1.01,
        ma1=5,
        ma2=13,
        n1=10,
        n2=21,
        obLevel1=60,
        obLevel2=53,
        osLevel1=-60,
        osLevel2=-53,
        rsi_period=14,
        percent_period=200,
        buy_limit1=5,
        buy_limit2=20,
        sell_limit1=95,
        sell_limit2=80,
    )

    def __init__(self):
        super().__init__()
        self.lag = Laguerre(self.datas[0],
                            short_gamma=self.p.short_gamma,
                            long_gamma=self.p.long_gamma,
                            pctile=self.p.pctile,
                            wrnpctile=self.p.wrnpctile,
                            lkbT=self.p.lkbT,
                            lkbB=self.p.lkbB)

        self.wvf = VIXFix(self.datas[0],
                          pd=self.p.pd,
                          bbl=self.p.bbl,
                          mult=self.p.mult,
                          lb=self.p.lb,
                          ph=self.p.ph,
                          pl=self.p.pl)

        ap = (self.datas[0].high + self.datas[0].low + self.datas[0].close) / 3
        esa = bt.ind.EMA(ap, period=self.p.n1)
        d = bt.ind.EMA(abs(ap - esa), period=self.p.n1)
        ci = (ap - esa) / (0.015 * d)
        self.tci = bt.ind.EMA(ci, period=self.p.n2)

        self.ma1 = bt.ind.ZeroLagExponentialMovingAverage(self.datas[0], period=self.p.ma1)
        self.ma2 = bt.ind.SMA(self.datas[0], period=self.p.ma2)

        self.rsi = bt.ind.RSI(self.datas[0], period=self.p.rsi_period)
        self.prank = bt.ind.PercentRank(self.rsi, period=self.p.percent_period) * 100

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
            if (self.wvf.lines.wvf > self.wvf.lines.bbands_top or self.wvf.lines.wvf > self.wvf.l.range_high) and self.lag.l.pctRankB <= self.lag.l.pctileB and self.prank <= self.p.buy_limit1:
                self.pending_buy = True
            elif self.pending_buy == True and self.lag.l.pctRankB >= self.lag.l.wrnpctileB and self.prank >= self.p.buy_limit2:
                self.pending_buy = False
                self.long(size=self.p.stake)
        if self.last_operation != "SELL":
            if self.lag.l.pctRankT >= self.p.pctile and self.prank >= self.p.sell_limit1:
                self.pending_sell = True
            elif self.pending_sell == True and self.lag.lines.pctRankT <= self.p.wrnpctile and self.prank <= self.p.sell_limit2:
                self.pending_sell = False
                self.short(size=self.p.stake)
