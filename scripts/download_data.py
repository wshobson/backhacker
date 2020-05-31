import os
from util.alphavantage import alpha_vantage_eod

# DOW_30 = [
#     'AAPL', 'AXP', 'BA', 'CAT', 'CSCO',
#     'CVX', 'DIS', 'DWDP', 'GE', 'GS',
#     'HD', 'IBM', 'INTC', 'JNJ', 'JPM',
#     'KO', 'MCD', 'MMM', 'MRK', 'MSFT',
#     'NKE', 'PFE', 'PG', 'TRV', 'UNH',
#     'UTX', 'V', 'VZ', 'WMT', 'XOM'
# ]

ETF = ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY', 'SPY']

for stock in ETF:
    eod_data = alpha_vantage_eod(
        [stock],
        compact=False,
        debug=False)

    df = eod_data.pop()[0]
    df = df.iloc[::-1]
    filename = stock + '.csv'
    df.to_csv(os.path.join(os.pardir, 'output/' + filename), header=False)

