import backtrader as bt
from strategies.BaseStrategy import BaseStrategy


class SMACross(BaseStrategy):
    def __init__(self):
        super().__init__()
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=20)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
