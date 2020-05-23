import sys
import argparse
import alpaca_backtrader_api
import backtrader as bt
import quantstats as qs
import matplotlib
from pandas import Series
from datetime import datetime
from functools import reduce

from analyzers.CashMarket import CashMarket

from strategies.Swing import Swing
from strategies.SMACross import SMACross
from strategies.GoldenCross import GoldenCross
from strategies.MultipleSMACross import MultipleSMACross
from strategies.StopLoss import StopLoss
from strategies.SimpleRSI import SimpleRSI
from strategies.DonchianChannels import DonchianChannels
from strategies.KeltnerChannel import KeltnerChannel
from strategies.ConnorsRSI import ConnorsRSI
from strategies.Momentum import Momentum
from strategies.TwoBarsDownFiveBarsHold import TwoBarsDownFiveBarsHold
from strategies.Extrema import Extrema
from strategies.BollingerBands import BollingerBands
from strategies.HeikinCandles import HeikinCandles
from strategies.TwoPeriodRSI import TwoPeriodRSI
from strategies.DoubleSevens import DoubleSevens

matplotlib.style.use('default')
qs.extend_pandas()


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def print_trade_analysis(analyzer):
    """
    Function to print the Technical Analysis results in a nice format.
    """
    total_open = round(deep_get(analyzer, 'total.open', default=0.0), 2)
    total_closed = round(deep_get(analyzer, 'total.closed', default=0.0), 2)
    total_won = round(deep_get(analyzer, 'won.total', default=0.0), 2)
    total_lost = round(deep_get(analyzer, 'lost.total', default=0.0), 2)
    win_streak = round(deep_get(analyzer, 'streak.won.longest', default=0.0), 2)
    lose_streak = round(deep_get(analyzer, 'streak.lost.longest', default=0.0), 2)
    pnl_net = round(deep_get(analyzer, 'pnl.net.total', default=0.0), 2)
    win_rate = round((total_won / total_closed) * 100, 2) if total_won > 0 and total_closed > 0 else 0.0

    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Win Rate', 'Win Streak', 'Losing Streak', 'P/L Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [win_rate, win_streak, lose_streak, pnl_net]

    print('-' * 65)
    for (h, r) in [(h1, r1), (h2, r2)]:
        print('|{:^15s}|{:^15s}|{:^15s}|{:^15s}|'.format(*h))
        print('|' + '-' * 15 + '|' + '-' * 15 + '|' + '-' * 15 + '|' + '-' * 15 + '|')
        print('|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|'.format(*r))
        print('-' * 65)


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
        '--strategy', type=str, default='golden_cross',
        help='The strategy to run')
    parser.add_argument(
        '--key-id', type=str, default=None,
        help='API key ID')
    parser.add_argument(
        '--secret-key', type=str, default=None,
        help='API secret key')
    parser.add_argument(
        '--is-backtest', type=str2bool, nargs='?', const=True, default=True,
        help='false if you want to do live paper trading, true will do a backtest')
    parser.add_argument(
        '--start-date', type=valid_date, default='2020-01-01',
        help='The start date - format YYYY-MM-DD')
    parser.add_argument(
        '--end-date', type=valid_date, default=datetime.now().strftime('%Y-%m-%d'),
        help='The end date - format YYYY-MM-DD')
    parser.add_argument(
        '--plot', type=str2bool, nargs='?', const=True, default=False,
        help='set to true to plot after backtest')
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
        help='set to true to use minutes as the time frame')

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    # available strategies
    strategies = {
        "swing": Swing,
        "sma_cross": SMACross,
        "golden_cross": GoldenCross,
        "multiple_sma_cross": MultipleSMACross,
        "stop_loss": StopLoss,
        "simple_rsi": SimpleRSI,
        "donchian_channels": DonchianChannels,
        "keltner_channel": KeltnerChannel,
        "conners_rsi": ConnorsRSI,
        "momentum": Momentum,
        "2bd_5bh": TwoBarsDownFiveBarsHold,
        "extrema": Extrema,
        "bollinger_bands": BollingerBands,
        "heikin": HeikinCandles,
        "2_period_rsi": TwoPeriodRSI,
        "double_7s": DoubleSevens,
    }

    args = parse_args()

    if args.strategy not in strategies:
        print('Invalid strategy, must select one of {}'.format(strategies.keys()))
        sys.exit()

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy=strategies[args.strategy], stake=args.stake)

    if args.is_backtest:
        cerebro.addobserver(bt.observers.Value)
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
        cerebro.addanalyzer(bt.analyzers.Returns)
        cerebro.addanalyzer(bt.analyzers.DrawDown)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        cerebro.addanalyzer(CashMarket, _name="cash_market")

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=args.key_id,
        secret_key=args.secret_key,
        paper=True,
        usePolygon=False)

    DataFactory = store.getdata
    time_frame = bt.TimeFrame.TFrame("Minutes") if args.is_minute else bt.TimeFrame.Days
    data1 = None

    if not args.is_backtest:
        data0 = DataFactory(
            dataname=args.symbol1,
            historical=False,
            timeframe=time_frame,
        )
        if args.symbol2:
            data1 = DataFactory(
                dataname=args.symbol2,
                historical=False,
                timeframe=time_frame,
            )

        broker = store.getbroker()
        cerebro.setbroker(broker)
    else:
        data0 = DataFactory(
            dataname=args.symbol1,
            historical=True,
            fromdate=args.start_date,
            todate=args.end_date,
            timeframe=time_frame,
        )

        if args.symbol2:
            data1 = DataFactory(
                dataname=args.symbol2,
                historical=True,
                fromdate=args.start_date,
                todate=args.end_date,
                timeframe=time_frame,
            )

    cerebro.adddata(data0)
    if data1 is not None:
        cerebro.adddata(data1)

    if args.is_backtest:
        cerebro.broker.setcash(args.cash)
        cerebro.broker.setcommission(commission=0.0)

    start_cash = cerebro.broker.getvalue()
    print('Starting Portfolio Value: ${:.2f}'.format(start_cash))

    results = cerebro.run()

    if args.is_backtest:
        portfolio_value = cerebro.broker.getvalue()
        pnl = portfolio_value - start_cash
        strat = results[0]

        # print the analyzers
        print('\nTrade Analysis Results for {} in {}:'.format(args.strategy, args.symbol1))
        print_trade_analysis(strat.analyzers.ta.get_analysis())
        print('Final Portfolio Value: ${:.2f}'.format(portfolio_value))
        print('P/L: ${:.2f}'.format(pnl))
        print('P/L %: {:.2f}%'.format((pnl / start_cash) * 100))
        print('Sharpe Ratio: {:.3f}'.format(strat.analyzers.sharperatio.get_analysis()['sharperatio'] or 0.0))
        print('SQN: {}'.format(round(strat.analyzers.sqn.get_analysis().sqn, 2)))
        print('Normalized Annual Return: {:.2f}%'.format(strat.analyzers.returns.get_analysis()['rnorm100'] or 0.0))
        print('Max Drawdown: {:.2f}%'.format(strat.analyzers.drawdown.get_analysis()['max']['drawdown'] or 0.0))

        if args.tearsheet:
            cash_market_analysis = strat.analyzers.cash_market.get_analysis()
            df = Series(cash_market_analysis, index=cash_market_analysis.keys())
            returns = qs.utils.to_returns(df)
            qs.reports.html(
                returns,
                benchmark=None,
                title='{} {} Strategy Tearsheet'.format(args.symbol1, args.strategy),
                output='output/{}-tearsheet.html'.format(args.symbol1))

        if args.plot:
            cerebro.plot(style='candlestick')
            # cerebro.plot()
