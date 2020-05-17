# import math
import backtrader as bt


class StopLoss(bt.Strategy):
    params = (('risk', 0.1),  # risk 10%
              ('stop_dist', 0.05))  # stop loss distance 5%

    def next(self):
        bar = len(self)
        # cash = self.broker.get_cash()

        if bar == 7:
            stop_price = (self.data.close[0] * (1 - self.p.stop_dist))
            # qty = math.floor((cash * self.p.risk) / (self.data.close[0] - stop_price))
            self.buy(data=self.data0)
            self.sell(exectype=bt.Order.Stop, data=self.data0, price=stop_price)

    def notify_trade(self, trade):
        date = self.data.datetime.datetime()
        if trade.isclosed:
            print('-' * 32, ' NOTIFY TRADE ', '-' * 32)
            print('{}, Avg Price: {}, Profit, Gross {}, Net {}'.format(
                date,
                trade.price,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
            print('-' * 80)
