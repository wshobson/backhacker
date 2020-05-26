import backtrader as bt


class StochasticRSI(bt.Indicator):
    lines = ('fastk', 'fastd',)

    params = dict(
        period=14,
        k_period=3,
        d_period=3,
        stoch_period=14,
        upper_band=80.0,
        lower_band=20.0,
    )

    def __init__(self, base_indicator):
        rsi_ll = bt.ind.Lowest(base_indicator, period=self.p.period)
        rsi_hh = bt.ind.Highest(base_indicator, period=self.p.period)
        stochrsi = (base_indicator - rsi_ll) / ((rsi_hh - rsi_ll) + 0.00001)

        self.l.fastk = k = bt.ind.SMA(100.0 * stochrsi, period=self.p.k_period)
        self.l.fastd = bt.ind.SMA(k, period=self.p.d_period)
