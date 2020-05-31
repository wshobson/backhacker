import quantstats as qs

SYMBOL = 'AAPL'

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

stock = qs.utils.download_returns(SYMBOL)

qs.reports.html(
    stock,
    'SPY',
    title='{} Strategy Tearsheet'.format(SYMBOL),
    output='output/{}-tearsheet.html'.format(SYMBOL))
