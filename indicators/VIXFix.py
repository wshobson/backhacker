import backtrader as bt
import statistics
import math


class VIXFix(bt.Indicator):
    params = dict(
        pd=22,  # LookBack Period Standard Deviation High
        bbl=20,  # Bollinger Band Length
        mult=2,  # Bollinger Band Standard Deviation Up
        lb=50,
        ph=0.85,
        pl=1.01,
        hp=False,
        sd=False,
    )

    lines = ("wvf", "bbands_top", "bbands_bot", "range_high", "range_low")

    def next(self):
        self.l.wvf[0] = 0.0
        self.l.bbands_top[0] = 0.0
        self.l.bbands_bot[0] = 0.0

        close_list = self.datas[0].close.get(size=self.p.pd).tolist()
        if len(close_list) == self.p.pd:
            max_close_list = max(close_list)
            self.l.wvf[0] = ((max_close_list - self.datas[0].low[0]) / max_close_list) * 100

            sdev = self.p.mult * statistics.stdev(self.l.wvf.get(size=self.p.bbl))
            datasum = math.fsum(self.l.wvf.get(size=self.p.bbl))
            midline = datasum / self.p.bbl

            self.l.bbands_top[0] = midline + sdev
            self.l.bbands_bot[0] = midline - sdev

            range_list = self.l.wvf.get(size=self.p.lb).tolist()
            if len(range_list) == self.p.lb:
                self.l.range_high[0] = max(range_list) * self.p.ph
                self.l.range_low[0] = min(range_list) * self.p.pl

            # print(self.lines.max[0], self.lines.wvf[0], self.lines.bbands_top[0], self.lines.bbands_bot[0], self.lines.range_high[0], self.lines.range_low[0])
