import backtrader as bt


class GoldenCross(bt.Strategy):
    params = dict(
        fast=50,
        slow=200,
        order_pct=0.95,
        stake=10,
    )

    def __init__(self):
        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.fast,
            plotname='50 day MA'
        )

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.slow,
            plotname='200 day MA'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma,
            self.slowma
        )

        self.dataclose = self.datas[0].close
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('{0},{1}'.format(dt.isoformat(), txt))

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

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if self.position.size == 0 and self.crossover > 0:
            # amount_to_invest = (self.p.order_pct * self.broker.cash)
            # self.size = math.floor(amount_to_invest / self.data.close)

            self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.buy(size=self.p.stake)

        if self.position.size > 0 > self.crossover:
            self.log('CLOSE CREATE, {0:8.2f}'.format(self.dataclose[0]))
            self.close(size=self.p.stake)
