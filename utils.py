import argparse
from functools import reduce
from datetime import datetime


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


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


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


# def send_telegram_message(message=""):
#     if ENV != "production":
#         return
#
#     base_url = "https://api.telegram.org/bot%s" % TELEGRAM.get("bot")
#     return requests.get("%s/sendMessage" % base_url, params={
#         'chat_id': TELEGRAM.get("channel"),
#         'text': message
#     })
