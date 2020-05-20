import backtrader as bt
from indicators.DonchianChannels import DonchianChannels


class DonchianHiLow(bt.Strategy):
    params = dict(
        stake=10,
    )

    def __init__(self):
        self.indicator = DonchianChannels()
        self.dataclose = self.datas[0].close
        self.order = None

    def next(self):
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:  # check if order is pending, if so, then break out
            return

        if self.data[0] > self.indicator.dch[0]:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(size=self.p.stake)
        elif self.data[0] < self.indicator.dcl[0]:
            self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.sell(size=self.p.stake)

    def log(self, txt, dt=None):
        # Logging function for the strategy.  'txt' is the statement and 'dt' can be used to specify a specific datetime
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

            self.bar_executed = len(self)  # when was trade executed
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
