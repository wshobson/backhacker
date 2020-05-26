from backtrader.sizers import PercentSizer


class FullMoney(PercentSizer):
    params = dict(
        percents=99,
    )
