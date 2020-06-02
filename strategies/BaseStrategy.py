from datetime import datetime

import backtrader as bt
from termcolor import colored

from config import ENV, DEVELOPMENT, PRODUCTION


class BaseStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.last_operation = "SELL"
        self.status = "DISCONNECTED"
        self.order = None
        self.buy_price_close = None
        self.buyprice = None
        self.buycomm = None
        self.soft_sell = False
        self.hard_sell = False
        self.bar_executed = None
        self.profit = 0

    def next(self):
        pass

    def reset_sell_indicators(self):
        self.soft_sell = False
        self.hard_sell = False
        self.buy_price_close = None

    def update_indicators(self):
        self.profit = 0
        if self.buy_price_close and self.buy_price_close > 0:
            self.profit = float(self.dataclose[0] - self.buy_price_close) / self.buy_price_close

    def log(self, txt, send_telegram=False, color=None):
        value = datetime.now()
        if len(self) > 0:
            value = self.data0.datetime.datetime()

        if color:
            txt = colored(txt, color)

        print('[{}] {}'.format(value.strftime("%y-%m-%d %H:%M"), txt))
        if send_telegram:
            # send_telegram_message(txt)
            pass

    def notify_data(self, data, status, *args, **kwargs):
        self.status = data._getstatusname(status)
        print(self.status)
        if status == data.LIVE:
            self.log("LIVE DATA - Ready to trade")

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        color = 'green'
        if trade.pnl < 0:
            color = 'red'

        self.log(colored('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(trade.pnl, trade.pnlcomm), color), True)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED/SUBMITTED')
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED', True)

        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.last_operation = "BUY"
                self.log('BUY EXECUTED, Price: {0:8.2f}, Cost: {1:8.2f}, Comm: {2:8.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm), True)
                if ENV == PRODUCTION:
                    print(order.__dict__)

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.last_operation = "SELL"
                self.reset_sell_indicators()
                self.log('SELL EXECUTED, {0:8.2f}, Cost: {1:8.2f}, Comm{2:8.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm), True)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected: Status {} - {}'.format(order.Status[order.status], self.last_operation), True)

        self.order = None

    def short(self, size=10):
        if self.last_operation == "SELL":
            return

        if ENV == DEVELOPMENT:
            self.log("Sell ordered: $%.2f" % self.dataclose[0], True)
            return self.sell(size=size)

        cash = self.broker.getcash()
        value = self.broker.getvalue()
        if cash <= 0:
            return

        amount = value * 0.99
        self.log("Sell ordered: $%.2f. Amount %.6f - $%.2f USDT" % (self.dataclose[0], amount, value), True)
        return self.sell(size=amount)

    def long(self, size=10):
        if self.last_operation == "BUY":
            return

        self.buy_price_close = self.dataclose[0]

        if ENV == DEVELOPMENT:
            self.log("Buy ordered: $%.2f" % self.dataclose[0], True)
            return self.buy(size=size)

        cash = self.broker.getcash()
        value = self.broker.getvalue()
        if cash <= 0:
            return

        price = self.dataclose[0]
        amount = (value / price) * 0.99  # Workaround to avoid precision issues
        self.log("Buy ordered: $%.2f. Amount %.6f. Balance $%.2f USDT" % (price, amount, value), True)
        return self.buy(size=amount)
