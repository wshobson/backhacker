import backtrader as bt

class ScalperAlert(bt.Indicator):
    lines = ('signal','stop')
    params = (('period', 4),)

    def next(self):
        signal = 0
        stop = 0
        # data = list(self.data.close)
        # data.extend([self.data.close(-i) for i in range(-1, -self.p.period, -1)])
        data = self.data.close.get(size=self.p.period)

        if len(data) < self.p.period:
            return
        if data[0] < data[1] < data[2] < data[3]:
            signal = 1
            stop = data[1]  # Stopping on first close in long trend
        if data[0] > data[1] > data[2] > data[3]:
            signal = -1
            stop = data[1]  # Stopping on first close in short trend

        self.lines.signal[0] = signal
        self.lines.stop[0] = stop
