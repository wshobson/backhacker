#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import sys
from datetime import datetime

import alpaca_backtrader_api
import backtrader as bt
import matplotlib
import pandas as pd
import pandas_datareader.data as web
import quantstats as qs

from analyzers.CashMarket import CashMarket
from config import ENV, PRODUCTION, ALPACA, ALPHAVANTAGE
from strategies.BollingerBands import BollingerBands
from strategies.BuyHold import BuyHold
from strategies.ConnorsRSI import ConnorsRSI
from strategies.DonchianChannels import DonchianChannels
from strategies.DoubleSevens import DoubleSevens
from strategies.ExtendedCross import ExtendedCross
from strategies.Extrema import Extrema
from strategies.GoldenCross import GoldenCross
from strategies.HeikinCandles import HeikinCandles
from strategies.KeltnerChannel import KeltnerChannel
from strategies.LaguerreRSI import LaguerreRSI
from strategies.LaguerreWilliams import LaguerreWilliams
from strategies.MACDGradient import MACDGradient
from strategies.Momentum import Momentum
from strategies.MultipleSMACross import MultipleSMACross
from strategies.PercentMA import PercentMA
from strategies.PercentMACDRSI import PercentMACDRSI
from strategies.RSICross import RSICross
from strategies.SMACross import SMACross
from strategies.SimpleRSI import SimpleRSI
from strategies.Slope import Slope
from strategies.StochasticCross import StochasticCross
from strategies.StopLoss import StopLoss
from strategies.Swing import Swing
from strategies.TripleCross import TripleCross
from strategies.TwoBarsDownFiveBarsHold import TwoBarsDownFiveBarsHold
from strategies.TwoPeriodRSI import TwoPeriodRSI
from strategies.VIXStretches import VIXStretches
from strategies.WeeklyHigh52 import WeeklyHigh52
from util.misc import print_trade_analysis, str2bool, valid_date

matplotlib.style.use('default')
qs.extend_pandas()


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Backhacker by Hobson Holdings')
    parser.add_argument(
        '--symbol1', type=str, default='SPY',
        help='Symbol you want to trade.')
    parser.add_argument(
        '--symbol2', type=str, default=None,
        help='Symbol you want to trade.')
    parser.add_argument(
        '--strategy', type=str, default='sma_cross',
        help='The strategy to run')
    parser.add_argument(
        '--start-date', type=valid_date, default='2020-01-01',
        help='The start date - format YYYY-MM-DD')
    parser.add_argument(
        '--end-date', type=valid_date, default=datetime.now().strftime('%Y-%m-%d'),
        help='The end date - format YYYY-MM-DD')
    parser.add_argument(
        '--plot', type=str2bool, nargs='?', const=True, default=False,
        help='set to true to plot after a backtest')
    parser.add_argument(
        '--stake', type=int, default=1,
        help='Stake to apply in each operation')
    parser.add_argument(
        '--cash', type=float, default=10000.0,
        help='Starting cash for backtesting')
    parser.add_argument(
        '--tearsheet',  type=str2bool, nargs='?', const=True, default=False,
        help='set to true to generate a Quantstats tearsheet')
    parser.add_argument(
        '--is-minute', type=str2bool, nargs='?', const=True, default=False,
        help='set to true to use minutes as the time frame instead of days')

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


def get_strategy(args):
    # available strategies
    strategies = {
        "buy_hold": BuyHold,
        "swing": Swing,
        "sma_cross": SMACross,
        "golden_cross": GoldenCross,
        "multiple_sma_cross": MultipleSMACross,
        "triple_cross": TripleCross,
        "stoch_cross": StochasticCross,
        "slope": Slope,
        "stop_loss": StopLoss,
        "simple_rsi": SimpleRSI,
        "laguerre_rsi": LaguerreRSI,
        "rsi_cross": RSICross,
        "extended_cross": ExtendedCross,
        "donchian_channels": DonchianChannels,
        "keltner_channel": KeltnerChannel,
        "connors_rsi": ConnorsRSI,
        "momentum": Momentum,
        "2bd_5bh": TwoBarsDownFiveBarsHold,
        "extrema": Extrema,
        "bollinger_bands": BollingerBands,
        "heikin": HeikinCandles,
        "2_period_rsi": TwoPeriodRSI,
        "double_7s": DoubleSevens,
        "vix_stretches": VIXStretches,
        "weekly_high_52": WeeklyHigh52,
        "percent_ma": PercentMA,
        "percent_macd_rsi": PercentMACDRSI,
        "macd_gradient": MACDGradient,
        "laguerre_williams": LaguerreWilliams,
    }

    if args.strategy not in strategies:
        print('Invalid strategy, must select one of {}'.format(strategies.keys()))
        sys.exit()

    return strategies[args.strategy]


def main():
    args = parse_args()

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy=get_strategy(args), stake=args.stake)

    if ENV != PRODUCTION:
        cerebro.addobserver(bt.observers.Value)
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
        cerebro.addanalyzer(bt.analyzers.Returns)
        cerebro.addanalyzer(bt.analyzers.DrawDown)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        cerebro.addanalyzer(CashMarket, _name="cash_market")

    time_frame = bt.TimeFrame.TFrame("Minutes") if args.is_minute else bt.TimeFrame.Days
    data1 = None

    if ENV == PRODUCTION:  # Live trading with Alpaca
        store = alpaca_backtrader_api.AlpacaStore(
            key_id=ALPACA.get("key"),
            secret_key=ALPACA.get("secret"),
            paper=True,
            usePolygon=False)

        DataFactory = store.getdata
        data0 = DataFactory(
            dataname=args.symbol1,
            historical=False,
            timeframe=time_frame)
        if args.symbol2:
            data1 = DataFactory(
                dataname=args.symbol2,
                historical=False,
                timeframe=time_frame)

        broker = store.getbroker()
        cerebro.setbroker(broker)
    else:  # Backtesting with AlphaVantage data
        df1 = web.get_data_alphavantage(
            args.symbol1,
            start=args.start_date,
            end=args.end_date,
            api_key=ALPHAVANTAGE.get("key"))
        df1.index = pd.to_datetime(df1.index)
        data0 = bt.feeds.PandasData(dataname=df1)

        if args.symbol2:
            df2 = web.get_data_alphavantage(
                args.symbol2,
                start=args.start_date,
                end=args.end_date,
                api_key=ALPHAVANTAGE.get("key"))
            df2.index = pd.to_datetime(df2.index)
            data1 = bt.feeds.PandasData(dataname=df2)

    cerebro.adddata(data0)
    if data1 is not None:
        cerebro.adddata(data1)

    if ENV != PRODUCTION:
        cerebro.broker.setcash(args.cash)
        cerebro.broker.setcommission(commission=0.0)

    start_cash = cerebro.broker.getvalue()
    print('Starting Portfolio Value: ${:.2f}'.format(start_cash))

    results = cerebro.run()

    if ENV != PRODUCTION:
        portfolio_value = cerebro.broker.getvalue()
        pnl = portfolio_value - start_cash
        strat = results[0]

        # print the analyzers
        print('\nTrade Analysis Results for {} in {}:'.format(args.strategy, args.symbol1))
        print('Final Portfolio Value: ${:.2f}'.format(portfolio_value))
        print('P/L: ${:.2f}'.format(pnl))
        print('P/L %: {:.2f}%'.format((pnl / start_cash) * 100))
        print('Sharpe Ratio: {:.3f}'.format(strat.analyzers.sharperatio.get_analysis()['sharperatio'] or 0.0))
        print('SQN: {}'.format(round(strat.analyzers.sqn.get_analysis().sqn, 2)))
        print('Normalized Annual Return: {:.2f}%'.format(strat.analyzers.returns.get_analysis()['rnorm100'] or 0.0))
        print('Max Drawdown: {:.2f}%'.format(strat.analyzers.drawdown.get_analysis()['max']['drawdown'] or 0.0))
        print_trade_analysis(strat.analyzers.ta.get_analysis())

        if args.tearsheet:
            cash_market_analysis = strat.analyzers.cash_market.get_analysis()
            df = pd.Series(cash_market_analysis, index=cash_market_analysis.keys())
            returns = qs.utils.to_returns(df)
            qs.reports.html(
                returns,
                benchmark=None,
                title='{} {} Strategy Tearsheet'.format(args.symbol1, args.strategy),
                output='output/{}-tearsheet.html'.format(args.symbol1))

        if args.plot:
            cerebro.plot(style='candlestick')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        time = datetime.now().strftime("%d-%m-%y %H:%M")
        print("Bot finished by user at {}".format(time))
        # send_telegram_message("Bot finished by user at %s" % time)
    except Exception as err:
        # send_telegram_message("Bot finished with error: %s" % err)
        print("Finished with error: ", err)
        raise
