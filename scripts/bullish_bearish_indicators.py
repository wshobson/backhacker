from datetime import datetime

import backtrader as bt

from util.alphavantage import alpha_vantage_eod
from util.scrape import obtain_parse_wiki_snp500


class TestStrategy(bt.Strategy):
    def __init__(self):
        self.inds = dict()
        self.inds['RSI'] = dict()
        self.inds['SMA'] = dict()

        for _, d in enumerate(self.datas):
            # RSI
            self.inds['RSI'][d._name] = dict()
            self.inds['RSI'][d._name]['value'] = bt.indicators.RSI(d, period=14)
            self.inds['RSI'][d._name]['bullish'] = self.inds['RSI'][d._name]['value'] > 50
            self.inds['RSI'][d._name]['bearish'] = self.inds['RSI'][d._name]['value'] < 50

            # SMA
            self.inds['SMA'][d._name] = dict()
            self.inds['SMA'][d._name]['value'] = bt.indicators.SMA(d, period=20)
            self.inds['SMA'][d._name]['bullish'] = d.close > self.inds['SMA'][d._name]['value']
            self.inds['SMA'][d._name]['bearish'] = d.close < self.inds['SMA'][d._name]['value']

    def stop(self):
        """
        Called when backtrader is finished the backtest. Here we will just get
        the final values at the end of testing for each indicator.
        """

        # Assuming all symbols are going to have the same data on the same days.
        # If that is not the case and you are mixing assets from different classes,
        # regions or exchanges, then you might want to consider adding an extra
        # column to the final results.
        output_str = ''
        output_str += 'Results from {} to {}\n'.format(self.datas[0].datetime.date(), datetime.today().strftime('%Y-%m-%d'))
        output_str += '-' * 80

        results = dict()
        for key, value in self.inds.items():
            results[key] = list()

            for nested_key, nested_value in value.items():
                if nested_value['bullish'] == True or nested_value['bearish'] == True:
                    results[key].append([nested_key, nested_value['bullish'][0],
                                         nested_value['bearish'][0], nested_value['value'][0]])

        headers = ['Indicator', 'Symbol', 'Bullish', 'Bearish', 'Value']
        output_str += '\n|{:^10s}|{:^10s}|{:^10s}|{:^10s}|{:^10s}|'.format(*headers)
        output_str += '\n|' + '-' * 10 + '|' + '-' * 10 + '|' + '-' * 10 + '|' + '-' * 10 + '|' + '-' * 10 + '|'

        for key, value in results.items():
            # print(value)
            value.sort(key=lambda x: x[0])  # Sort by Ticker

            for result in value:
                output_str += '\n|{:^10s}|{:^10s}|{:^10}|{:^10}|{:^10.2f}|'.format(key, *result)

        with open('output/screener-output.txt', 'w') as text_file:
            print(output_str, file=text_file)

        print(output_str)


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    sp500 = obtain_parse_wiki_snp500()
    eod_data = alpha_vantage_eod(
        sp500[:10],  # remove the slice for a full test, as it requires a long runtime
        compact=True,
        debug=False)

    for i in range(len(eod_data)):
        feed = bt.feeds.PandasData(
            dataname=eod_data[i][0],
            name=eod_data[i][1],
            timeframe=bt.TimeFrame.Days,
            compression=1,
        )

        cerebro.adddata(feed)

    print('\nStarting Analysis')
    print('-' * 80)

    cerebro.run()
