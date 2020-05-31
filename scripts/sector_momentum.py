import os
from datetime import datetime

import backtrader as bt
import matplotlib
import numpy as np
from scipy.stats import linregress

matplotlib.use('Qt5Agg')

START_DATE = '2000-01-01'
START = datetime.strptime(START_DATE, '%Y-%m-%d')
END_DATE = '2020-05-29'
END = datetime.strptime(END_DATE, '%Y-%m-%d')
ETF_TICKERS = ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY']


def momentum_func(self, price_array):
    r = np.log(price_array)
    slope, _, rvalue, _, _ = linregress(np.arange(len(r)), r)
    annualized = (1 + slope) ** 252
    return annualized * (rvalue ** 2)


class Momentum(bt.ind.OperationN):
    lines = ('trend',)
    params = dict(period=90)
    func = momentum_func


class Strategy(bt.Strategy):
    params = dict(
        momentum=Momentum,
        momentum_period=180,
        num_positions=2,
        when=bt.timer.SESSION_START,
        timer=True,
        monthdays=[1],
        monthcarry=True,
        printlog=True
    )

    def log(self, txt, dt=None, doprint=False):
        """ Logging function for this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.i = 0
        self.securities = self.datas[1:]
        self.inds = {}

        self.add_timer(
            when=self.p.when,
            monthdays=self.p.monthdays,
            monthcarry=self.p.monthcarry
        )

        for security in self.securities:
            self.inds[security] = self.p.momentum(security,
                                                  period=self.p.momentum_period)

    def notify_timer(self, timer, when, *args, **kwargs):
        if self._getminperstatus() < 0:
            self.rebalance()

    def rebalance(self):
        rankings = list(self.securities)
        rankings.sort(key=lambda s: self.inds[s][0], reverse=True)
        pos_size = 1 / self.p.num_positions

        # Sell stocks no longer meeting ranking filter.
        for i, d in enumerate(rankings):
            if self.getposition(d).size:
                if i > self.p.num_positions:
                    self.close(d)

        # Buy and rebalance stocks with remaining cash
        for i, d in enumerate(rankings[:self.p.num_positions]):
            self.order_target_percent(d, target=pos_size)

    def next(self):
        self.notify_timer(self, self.p.timer, self.p.when)

    def stop(self):
        self.log('| %2d | %2d |  %.2f |' %
                 (self.p.momentum_period,
                  self.p.num_positions,
                  self.broker.getvalue()),
                 doprint=True)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.0)

    spy_file = os.path.join(os.pardir, 'output/SPY.csv')
    benchdata = bt.feeds.GenericCSVData(
        dataname=spy_file,
        dtformat='%Y-%m-%d',
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1,
        name='SPY',
        plot=True,
    )

    cerebro.adddata(benchdata)

    for stock in ETF_TICKERS:
        filename = os.path.join(os.pardir, 'output/' + stock + '.csv')
        data = bt.feeds.GenericCSVData(
            dataname=filename,
            dtformat='%Y-%m-%d',
            datetime=0,
            high=2,
            low=3,
            open=1,
            close=4,
            volume=5,
            openinterest=-1,
            name=stock,
            plot=False,
        )

        print("Adding ticker: {}".format(stock))
        data.plotinfo.plotmaster = benchdata
        cerebro.adddata(data)

    cerebro.addobserver(bt.observers.Value)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    stop = len(ETF_TICKERS) + 1
    cerebro.optstrategy(Strategy,
                        momentum_period=range(50, 300, 50),
                        num_positions=range(1, stop))

    cerebro.run(stdstats=False, tradehistory=False)
