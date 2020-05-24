import backtrader as bt


class Laguerre(bt.Indicator):
    params = dict(
        short_gamma=0.4,
        long_gamma=0.8,
        pctile=90,
        wrnpctile=70,
        lkbT=200,
        lkbB=200,
    )

    lines = ("pctRankT", "pctRankB", "pctileB", "wrnpctileB", "ppoT", "ppoB")

    lmas_l0, lmas_l1, lmas_l2, lmas_l3 = 0.0, 0.0, 0.0, 0.0
    lmal_l0, lmal_l1, lmal_l2, lmal_l3 = 0.0, 0.0, 0.0, 0.0

    def next(self):

        # lmas
        lmas0_1 = self.lmas_l0  # cache previous intermediate values
        lmas1_1 = self.lmas_l1
        lmas2_1 = self.lmas_l2

        g = self.p.short_gamma  # avoid more lookups
        self.lmas_l0 = l0 = (1.0 - g) * (self.datas[0].high + self.datas[0].low) / 2 + g * lmas0_1
        self.lmas_l1 = l1 = -g * l0 + lmas0_1 + g * lmas1_1
        self.lmas_l2 = l2 = -g * l1 + lmas1_1 + g * lmas2_1
        self.lmas_l3 = l3 = -g * l2 + lmas2_1 + g * self.lmas_l3

        self.lmas = lmas = (self.lmas_l0 + 2 * self.lmas_l1 + 2 * self.lmas_l2 + self.lmas_l3) / 6

        # lmal
        lmal0_1 = self.lmal_l0  # cache previous intermediate values
        lmal1_1 = self.lmal_l1
        lmal2_1 = self.lmal_l2

        g = self.p.long_gamma  # avoid more lookups
        self.lmal_l0 = l0 = (1.0 - g) * (self.datas[0].high + self.datas[0].low) / 2 + g * lmal0_1
        self.lmal_l1 = l1 = -g * l0 + lmal0_1 + g * lmal1_1
        self.lmal_l2 = l2 = -g * l1 + lmal1_1 + g * lmal2_1
        self.lmal_l3 = l3 = -g * l2 + lmal2_1 + g * self.lmal_l3

        lmal = (self.lmal_l0 + 2 * self.lmal_l1 + 2 * self.lmal_l2 + self.lmal_l3) / 6

        self.l.pctileB[0] = self.p.pctile * -1
        self.l.wrnpctileB[0] = self.p.wrnpctile * -1

        self.l.ppoT[0] = (lmas - lmal) / lmal * 100
        self.l.ppoB[0] = (lmal - lmas) / lmal * 100

        ppoT_list = self.l.ppoT.get(size=self.p.lkbT).tolist()
        if len(ppoT_list) == self.p.lkbT:
            self.l.pctRankT[0] = sum(self.l.ppoT[0] >= i for i in ppoT_list) / len(ppoT_list) * 100

        ppoB_list = self.l.ppoB.get(size=self.p.lkbB).tolist()
        if len(ppoB_list) == self.p.lkbB:
            self.l.pctRankB[0] = sum(self.l.ppoB[0] >= i for i in ppoB_list) / len(ppoB_list) * -100
