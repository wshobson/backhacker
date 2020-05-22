import backtrader as bt


class CashMarket(bt.analyzers.Analyzer):
    """
    Analyzer returning cash and market values
    """
    def start(self):
        super(CashMarket, self).start()

    def create_analysis(self):
        self.rets = {}
        self.vals = 0.0

    def notify_cashvalue(self, cash, value):
        self.vals = value
        self.rets[self.strategy.datetime.datetime()] = self.vals

    def get_analysis(self):
        return self.rets