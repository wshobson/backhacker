import backtrader as bt
from indicators.Momentum import Momentum as MomentumInd


class Momentum(bt.Strategy):
    params = dict(
        stake=10,  # just need for other strategies, not used here
    )

    def __init__(self):
        self.i = 0
        self.inds = {}
        self.spy = self.datas[0]
        self.stocks = self.datas[1:]

        # TODO: figure out a way to support this with SPY 200 MA
        self.spy_sma200 = bt.indicators.SimpleMovingAverage(self.spy.close, period=200)

        for d in self.stocks:
            self.inds[d] = {}
            self.inds[d]["momentum"] = MomentumInd(d.close, period=90)
            self.inds[d]["sma100"] = bt.indicators.SimpleMovingAverage(d.close, period=100)
            self.inds[d]["atr20"] = bt.indicators.ATR(d, period=20)

    def prenext(self):
        # call next() even when data is not available for all tickers
        self.next()

    def next(self):
        if self.i % 5 == 0:
            self.rebalance_portfolio()
        if self.i % 10 == 0:
            self.rebalance_positions()
        self.i += 1

    def rebalance_portfolio(self):
        # only look at data that we can have indicators for
        self.rankings = list(filter(lambda x: len(x) > 100, self.stocks))
        self.rankings.sort(key=lambda x: self.inds[x]["momentum"][0])
        num_stocks = len(self.rankings)

        # sell stocks based on criteria
        for i, d in enumerate(self.rankings):
            if self.getposition(self.data).size:
                if i > num_stocks * 0.2 or d < self.inds[d]["sma100"]:
                    self.close(d)

        if self.spy < self.spy_sma200:
            return

        # buy stocks with remaining cash
        for i, d in enumerate(self.rankings[:int(num_stocks * 0.2)]):
            cash = self.broker.get_cash()
            value = self.broker.get_value()
            if cash <= 0:
                break
            if not self.getposition(self.data).size:
                size = value * 0.001 / self.inds[d]["atr20"]
                self.buy(d, size=size)

    def rebalance_positions(self):
        num_stocks = len(self.rankings)

        if self.spy < self.spy_sma200:
            return

        # rebalance all stocks
        for i, d in enumerate(self.rankings[:int(num_stocks * 0.2)]):
            cash = self.broker.get_cash()
            value = self.broker.get_value()
            if cash <= 0:
                break
            size = value * 0.001 / self.inds[d]["atr20"]
            self.order_target_size(d, size)
