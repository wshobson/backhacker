import backtrader as bt


class MultipleSmaCross(bt.SignalStrategy):
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime[0]
        dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

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

    # def notify_order(self, order):
    #     if order.status in [order.Completed, order.Cancelled, order.Rejected]:
    #         print('Created: {} Price: {} Size: {}'.format(
    #             bt.num2date(order.created.dt),
    #             order.executed.price,
    #             order.executed.size))
    #         print('-' * 80)
    #
    #     print('{}: Order ref: {} / Type {} / Status {}'.format(
    #         self.data.datetime.date(0),
    #         order.ref, 'Buy' * order.isbuy() or 'Sell',
    #         order.getstatusname()))

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        # if status == data.LIVE:
        #     self.counttostop = self.p.stopafter
        #     self.datastatus = 1

    def stop(self):
        print('==================================================')
        print('Starting Value - %.2f' % self.broker.startingcash)
        print('Ending   Value - %.2f' % self.broker.getvalue())
        print('==================================================')

    def __init__(self):
        sma1 = bt.ind.SMA(self.data0, period=self.p.pfast)
        sma2 = bt.ind.SMA(self.data0, period=self.p.pslow)
        self.crossover0 = bt.ind.CrossOver(sma1, sma2)

        sma1 = bt.ind.SMA(self.data1, period=self.p.pfast)
        sma2 = bt.ind.SMA(self.data1, period=self.p.pslow)
        self.crossover1 = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        # if fast crosses slow to the upside
        # print('{}: O {}, H {}, L {}, C {}'.format(
        #     self.data0.datetime.datetime(),
        #     self.data0.open[0],
        #     self.data0.high[0],
        #     self.data0.low[0],
        #     self.data0.close[0]))
        #
        # print('{}: O {}, H {}, L {}, C {}'.format(
        #     self.data1.datetime.datetime(),
        #     self.data1.open[0],
        #     self.data1.high[0],
        #     self.data1.low[0],
        #     self.data1.close[0]))

        if not self.getposition(self.data0).size and self.crossover0 > 0:
            self.buy(data=self.data0)  # enter long

        if not self.getposition(self.data1).size and self.crossover1 > 0:
            self.buy(data=self.data1)  # enter long

        # in the market & cross to the downside
        if self.getposition(self.data0).size and self.crossover0 <= 0:
            self.close(data=self.data0)  # close long position
        # in the market & cross to the downside
        if self.getposition(self.data1).size and self.crossover1 <= 0:
            self.close(data=self.data1)  # close long position
