import backtrader as bt


class KeltnerChannel(bt.Indicator):
    lines = ('mid', 'upper', 'lower',)
    params = dict(
        ema=20,
        atr=2,
    )

    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(
        mid=dict(ls='--'),  # dashed line
        upper=dict(_samecolor=True),  # use same color as prev line (mid)
        lower=dict(_samecolor=True),  # use same color as prev line (upper)
    )

    def __init__(self):
        self.l.mid = bt.ind.EMA(period=self.p.ema)
        self.l.upper = self.l.mid + bt.ind.ATR(period=self.p.ema) * self.p.atr
        self.l.lower = self.l.mid - bt.ind.ATR(period=self.p.ema) * self.p.atr
