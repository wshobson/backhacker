from strategies.BaseStrategy import BaseStrategy
import backtrader as bt


class StopLoss(BaseStrategy):
    def next(self):
        if len(self) % 7 == 0:  # every 7th bar, for demonstration only
            stop_dist = 0.05
            stop_price = (self.data.close[0] * (1 - stop_dist))
            self.buy(size=self.p.stake)
            self.sell(exectype=bt.Order.Stop, price=stop_price, size=self.p.stake)
