import sys
import argparse
import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime

from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from strategies.MultipleSmaCross import MultipleSmaCross
from strategies.StopLoss import StopLoss
from strategies.SimpleRsi import SimpleRsi


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
        '--is-minute', type=str2bool, nargs='?', const=True, default=False,
        help='set to true to use minutes as the time frame')

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    # available strategies
    strategies = {
        "golden_cross": GoldenCross,
        "buy_hold": BuyHold,
        "multiple_sma_cross": MultipleSmaCross,
        "stop_loss": StopLoss,
        "simple_rsi": SimpleRsi,
    }

    args = parse_args()

    if args.strategy not in strategies:
        print("Invalid strategy, must select one of {}".format(strategies.keys()))
        sys.exit()

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy=strategies[args.strategy])
    cerebro.addsizer(bt.sizers.PercentSizer, percents=50)

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=args.key_id,
        secret_key=args.secret_key,
        paper=True,
        usePolygon=False)

    DataFactory = store.getdata
    data1 = None

    if not args.is_backtest:
        data0 = DataFactory(
            dataname=args.symbol1,
            historical=False,
            timeframe=bt.TimeFrame.TFrame("Minutes") if args.is_minute else bt.TimeFrame.Days,
        )
        if args.symbol2:
            data1 = DataFactory(
                dataname=args.symbol2,
                historical=False,
                timeframe=bt.TimeFrame.TFrame("Minutes") if args.is_minute else bt.TimeFrame.Days,
            )

        broker = store.getbroker()
        cerebro.setbroker(broker)
    else:
        data0 = DataFactory(
            dataname=args.symbol1,
            historical=True,
            fromdate=args.start_date,
            todate=args.end_date,
            timeframe=bt.TimeFrame.TFrame("Minutes") if args.is_minute else bt.TimeFrame.Days,
        )

        if args.symbol2:
            data1 = DataFactory(
                dataname=args.symbol2,
                historical=True,
                fromdate=args.start_date,
                todate=args.end_date,
                timeframe=bt.TimeFrame.TFrame("Minutes") if args.is_minute else bt.TimeFrame.Days,
            )

    cerebro.adddata(data0)
    if data1:
        cerebro.adddata(data1)

    if args.is_backtest:
        cerebro.broker.setcash(10000.0)
        cerebro.broker.setcommission(commission=0.0)

    start_cash = cerebro.broker.getvalue()
    print('Starting Portfolio Value: $%.2f' % start_cash)

    cerebro.run()

    portfolio_value = cerebro.broker.getvalue()
    pnl = portfolio_value - start_cash
    print('Final Portfolio Value: $%.2f' % portfolio_value)
    print('P/L: $%.2f' % pnl)
    print('P/L: {}%'.format((pnl / start_cash) * 100))

    if args.plot:
        cerebro.plot(style='candlestick')
