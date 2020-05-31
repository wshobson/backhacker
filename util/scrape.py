import bs4
import requests


def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P500
    constituents.
    """
    response = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    symbols_list = soup.select('table')[0].select('tr')[1:]

    tickers = []
    for _, symbol in enumerate(symbols_list):
        tds = symbol.select('td')
        tickers.append(tds[0].select('a')[0].text)
    return [x for x in tickers if '.' not in x]
