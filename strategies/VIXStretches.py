import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class VIXStretches(BaseStrategy):
    """
    Implementation of the VIX Stretches strategy from Larry Connor's
    Short-Term Strategies book, Chapter 12
    Algorithm:
        1. The SPY is above its 200-day MA.
        2. The VIX is stretched 5% or more above its 10-day MA for 3 or more days.
           If this occurs, we’ll buy the market on the close.
        3. Exit when the SPY closes above a 2-period RSI reading of 65 or more.
    """
    params = dict(
        stake=10,
        spy_sma=200,
        vix_sma=10,
        n_period=5,
        stretched_pct=5,
        k_periods=3,
        rsi_period=2,
        rsi_bound=65,
    )

    def __init__(self):
        super().__init__()
        self.vixdataclose = self.data1.close
        self.spydataclose = self.data0.close
        self.spysma = bt.ind.SMA(self.data0, period=self.p.spy_sma)
        self.spyrsi = bt.ind.RSI_Safe(self.data0, period=self.p.rsi_period)
        self.vixstd = bt.ind.StdDev(self.data1, period=self.p.n_period)
        self.vixsma = bt.ind.SMA(self.vixstd, period=self.p.vix_sma)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.spydataclose[0]))

        if self.order:
            return

        if not self.getposition(self.data0):
            vix_stretched = all(self.vixstd[i] > (self.vixsma[i] * (1 + self.p.stretched_pct / 100.0)) for i in range(0, -self.p.k_periods, -1))
            if self.spydataclose[0] > self.spysma[0] and vix_stretched:
                self.log('BUY CREATE {0:8.2f}'.format(self.spydataclose[0]))
                self.order = self.buy(data=self.data0, size=self.p.stake)
        else:
            if self.spyrsi[0] >= self.p.rsi_bound:
                self.log('CLOSE CREATE, {0:8.2f}'.format(self.spydataclose[0]))
                self.order = self.close(data=self.data0, size=self.p.stake)
