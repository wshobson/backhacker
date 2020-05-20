import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class GoldenCross(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=50,
            plotname='50 day MA'
        )

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=200,
            plotname='200 day MA'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma,
            self.slowma
        )

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if self.position.size == 0 and self.crossover > 0:
            # amount_to_invest = (0.05 * self.broker.cash)
            # self.size = math.floor(amount_to_invest / self.data.close)

            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.buy(size=self.p.stake)

        if self.position.size > 0 > self.crossover:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.close(size=self.p.stake)
