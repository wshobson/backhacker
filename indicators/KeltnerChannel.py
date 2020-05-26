import backtrader as bt


class KeltnerChannel(bt.Indicator):
    """
      Keltner Channels are a technical indicator that combines an exponential
      moving average with volatility-based envelopes set above and below the EMA
      at a fixed percentage of the same duration. Keltner Channels aim to identify
      the underlying price trend and over-extended conditions.
          Formula:
          - https://en.wikipedia.org/wiki/Keltner_channel
          See also:
          - https://analyzingalpha.com/keltner-channels
      """
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
