import backtrader as bt

from indicators.KeltnerChannel import KeltnerChannel


class Squeeze(bt.Indicator):
    """
        The Squeeze, developed and popularized by John Carter, looks at the relationship
        between Bollinger Bands and Keltner Channels to help identify consolidations and
        signal when prices are likely to break out (whether up or down).

        The squeeze formula basically boils down to this:

        Squeeze = (BBDevs X StdDev(close, period)) – (KCDevs X ATR(period))
    """
    lines = ('squeeze', 'entered', 'exited',)
    params = dict(
        period=20,
        bbdev=2.0,
        kdev=1.5,
        movav=bt.ind.MovAv.Simple
    )
    plotinfo = dict(subplot=True)

    def __init__(self):
        bb = bt.ind.BollingerBands(period=self.p.period, devfactor=self.p.devfactor, movav=self.p.movav)
        kc = KeltnerChannel(period=self.p.period, factor=self.p.kdev)
        self.l.squeeze = bb.top - kc.upper
        self.l.entered = self.l.squeeze <= 0 < self.l.squeeze[1]
        self.l.exited = self.l.squeeze > 0 >= self.l.squeeze[1]
