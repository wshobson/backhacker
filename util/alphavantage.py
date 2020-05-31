import os
import time
import pandas as pd

from alpha_vantage.timeseries import TimeSeries

API_KEY = os.environ['ALPHAVANTAGE_API_KEY']


def alpha_vantage_eod(symbol_list, compact=False, debug=False):
    """
    Helper function to download AlphaVantage Data.

    This will return a nested list with each entry containing:
        [0] pandas dataframe
        [1] the name of the feed.
    """
    data_list = list()

    size = 'compact' if compact else 'full'

    count = 0
    total = len(symbol_list)

    for symbol in symbol_list:
        count += 1

        print('\nDownloading: {}'.format(symbol))
        print('Symbol: {} of {}'.format(count, total, symbol))
        print('-' * 80)

        alpha_ts = TimeSeries(key=API_KEY, output_format='pandas')

        data, meta_data = alpha_ts.get_daily(symbol=symbol, outputsize=size)

        data.index = pd.to_datetime(data.index)
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        if debug:
            print(data)

        data_list.append((data, symbol))

        print('Sleeping |', end='', flush=True)
        for x in range(12):
            print('=', end='', flush=True)
            time.sleep(1)
        print('| Done!')

    return data_list
