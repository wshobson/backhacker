from strategies.BaseStrategy import BaseStrategy


class BuyHold(BaseStrategy):
    def nextstart(self):
        size = int(self.broker.get_cash() / self.data)
        self.buy(size=size)
