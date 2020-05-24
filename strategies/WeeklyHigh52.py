import backtrader as bt
from strategies.BaseStrategy import BaseStrategy
from indicators.DonchianChannels import DonchianChannels as DonchianChannelsInd


class WeeklyHigh52(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.indicator = DonchianChannelsInd(period=240)

    def next(self):
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order:
            return

        if self.indicator.buysig[0]:
            if self.position.size > 0:
                return
            elif self.position.size < 0:
                self.close(size=self.p.stake)
            self.log('BUY BRACKET CREATE {0:8.2f}'.format(self.dataclose[0]))
            self.order = self.buy_bracket(size=self.p.stake,
                                          exectype=bt.Order.Market,
                                          stopprice=self.dataclose[0] * 0.02,
                                          limitprice=self.dataclose[0] * 1.05)
        elif self.indicator.sellsig[0]:
            if self.position.size < 0:
                return
            elif self.position.size > 0:
                self.close(size=self.p.stake)
            # self.log('SELL BRACKET CREATE, {0:8.2f}'.format(self.dataclose[0]))
            # self.order = self.sell_bracket(size=self.p.stake,
            #                                exectype=bt.Order.Market,
            #                                stopprice=self.dataclose[0] * 1.1,
            #                                limitprice=self.dataclose[0] * 0.98)
