import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class DoubleSevens(BaseStrategy):
    """
    Implementation of the Double 7's strategy from Larry Connor's
    Short-Term Strategies book, Chapter 10
    Algorithm:
        1. The SPY is above its 200-day moving average or SPY is above its 50-day MA
        2. The SPY closes at a X-day low, buy.
        3. If the SPY closes at a X-day high, sell your long position.
    """
    params = dict(
        stake=10,
        period=8,
        sma=70,
        stop_loss=0.05,
    )

    def __init__(self):
        super().__init__()
        self.stop_loss = 0
        # self.shares = 0
        self.sma200 = bt.ind.SMA(self.datas[0], period=200)
        self.sma = bt.ind.SMA(self.datas[0], period=self.p.sma)
        self.high_bar = bt.ind.Highest(self.datas[0], period=self.p.period)
        self.low_bar = bt.ind.Lowest(self.datas[0], period=self.p.period)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if (self.dataclose[0] > self.sma200[0] or self.dataclose[0] > self.sma[0]) and self.dataclose[0] == self.low_bar[0]:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))

                # self.shares = int(self.broker.get_cash() / self.dataclose[0])
                self.order = self.buy(size=self.p.stake)
                # self.stop_loss = (1 - self.p.stop_loss) * self.dataclose[0]
                self.stop_loss = 0 * self.dataclose[0]  # no stop loss
        else:
            if self.dataclose[0] == self.high_bar[0] or self.data.low[0] < self.stop_loss:
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell(size=self.p.stake)
