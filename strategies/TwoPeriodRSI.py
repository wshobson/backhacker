import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class TwoPeriodRSI(BaseStrategy):
    """
    Implementation of the 2-period RSI strategy from Larry Connor's
    Short-Term Strategies book, Chapter 9
    Algorithm:
        1. The SPY is above its 200-day MA.
        2. If the 2-period RSI of the SPY closes below 5, buy.
        3. If the SPY closes above its 5-period MA, sell your long position.
    """
    def __init__(self):
        super().__init__()
        self.rsi = bt.indicators.RSI_Safe(self.datas[0], period=2)
        self.sma5 = bt.ind.SMA(self.datas[0], period=5)
        self.sma200 = bt.ind.SMA(self.datas[0], period=200)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma200[0] and self.rsi[0] < 5:
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.buy(size=self.p.stake)
        else:
            if self.dataclose[0] > self.sma5[0]:
                self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.close(size=self.p.stake)
