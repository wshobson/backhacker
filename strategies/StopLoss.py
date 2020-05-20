# import math
import backtrader as bt


class StopLoss(bt.Strategy):
    params = dict(
        risk=0.1,  # risk 10%
        stop_dist=0.05,  # stop loss distance 5%
        stake=10,
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def next(self):
        if len(self) % 7 == 0:  # every 7th bar, for demonstration only
            stop_price = (self.data.close[0] * (1 - self.p.stop_dist))
            self.buy(size=self.p.stake)
            self.sell(exectype=bt.Order.Stop, price=stop_price, size=self.p.stake)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('{0}, {1}'.format(dt.isoformat(), txt))

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))

    def notify_order(self, order):
        # 1. If order is submitted/accepted, do nothing
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {0:8.2f}, Cost: {1:8.2f}, Comm: {2:8.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, {0:8.2f}, Cost: {1:8.2f}, Comm{2:8.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))

        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
