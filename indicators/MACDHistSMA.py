import backtrader as bt


class MACDHistSMA(bt.Indicator):
    lines = ('histo',)

    params = dict(
        period=14,
    )

    def __init__(self):
        MACD = bt.ind.MACDHisto()
        self.l.histo = bt.indicators.MovingAverageSimple(MACD.histo, period=self.p.period)