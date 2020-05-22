from strategies.BaseStrategy import BaseStrategy
import backtrader as bt


class BollingerBands(BaseStrategy):
    params = dict(
        stake=10,
        bbands_period=20,
    )

    def __init__(self):
        super().__init__()

        self.redline = None
        self.blueline = None

        # Add a BBand indicator
        self.bband = bt.indicators.BBands(self.datas[0], period=self.params.bbands_period)

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if self.dataclose < self.bband.lines.bot and not self.position:
            self.redline = True

        if self.dataclose > self.bband.lines.top and self.position:
            self.blueline = True

        if self.dataclose > self.bband.lines.mid and not self.position and self.redline:
            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy(size=self.p.stake)

        if self.dataclose > self.bband.lines.top and not self.position:
            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy(size=self.p.stake)

        if self.dataclose < self.bband.lines.mid and self.position and self.blueline:
            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            self.blueline = False
            self.redline = False
            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell(size=self.p.stake)
