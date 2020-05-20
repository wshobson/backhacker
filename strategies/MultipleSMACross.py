import backtrader as bt


class MultipleSMACross(bt.SignalStrategy):
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30,  # period for the slow moving average
        stake=10,
    )

    def __init__(self):
        sma1 = bt.ind.SMA(self.data0, period=self.p.pfast)
        sma2 = bt.ind.SMA(self.data0, period=self.p.pslow)
        self.crossover0 = bt.ind.CrossOver(sma1, sma2)

        sma1 = bt.ind.SMA(self.data1, period=self.p.pfast)
        sma2 = bt.ind.SMA(self.data1, period=self.p.pslow)
        self.crossover1 = bt.ind.CrossOver(sma1, sma2)

        self.dataclose = self.datas[0].close
        self.order = None

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

        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def stop(self):
        print('==================================================')
        print('Starting Value - %.2f' % self.broker.startingcash)
        print('Ending   Value - %.2f' % self.broker.getvalue())
        print('==================================================')

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if not self.getposition(self.data0).size and self.crossover0 > 0:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(data=self.data0, size=self.p.stake)  # enter long

        if not self.getposition(self.data1).size and self.crossover1 > 0:
            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy(data=self.data1, size=self.p.stake)  # enter long

        # in the market & cross to the downside
        if self.getposition(self.data0).size and self.crossover0 <= 0:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.close(data=self.data0, size=self.p.stake)  # close long position
        # in the market & cross to the downside
        if self.getposition(self.data1).size and self.crossover1 <= 0:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.close(data=self.data1, size=self.p.stake)  # close long position
