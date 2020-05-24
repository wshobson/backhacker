import backtrader as bt


class DonchianChannels(bt.Indicator):
    """
    Params Note:
      - `lookback` (default: -1)
        If `-1`, the bars to consider will start 1 bar in the past and the
        current high/low may break through the channel.
        If `0`, the current prices will be considered for the Donchian
        Channel. This means that the price will **NEVER** break through the
        upper/lower channel bands.

        Definition:
          - https://en.wikipedia.org/wiki/Donchian_channel
          See also:
          - https://analyzingalpha.com/backtrader-backtesting-trading-strategies
    """

    alias = ('DCH', 'DonchianChannel',)

    lines = ('dcm', 'dch', 'dcl', 'buysig', 'sellsig', 'exitlong', 'exitshort',)  # dc middle, dc high, dc low
    params = dict(
        period=20,
        lookback=-1,  # consider current bar or not
    )

    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(
        dcm=dict(ls='--'),  # dashed line
        dch=dict(_samecolor=True),  # use same color as prev line (dcm)
        dcl=dict(_samecolor=True),  # use same color as prev line (dch)
    )

    def __init__(self):
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        self.l.dch = bt.ind.Highest(hi, period=self.p.period)
        self.l.dcl = bt.ind.Lowest(lo, period=self.p.period)
        self.l.dcm = (self.l.dch + self.l.dcl) / 2.0  # avg of the above
        self.l.buysig = self.data.close > self.l.dch
        self.l.sellsig = self.data.close < self.l.dcl
        self.l.exitlong = self.data.close < self.l.dcm
        self.l.exitshort = self.data.close > self.l.dcm
