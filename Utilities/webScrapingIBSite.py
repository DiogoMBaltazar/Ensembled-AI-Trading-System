import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re

# Script returns a dictionary with all the NASDAQ Equities listed on the IB website.
# Later, will be updated to retrieve futures as well.

end_page = 43

start_ticker = "d>"
end_ticker = "</t"

start_name = '">'
end_name = "</a"

tickers = []
names = []

for page_idx in range(1, end_page + 1):
    URL = requests.get ('https://www.interactivebrokers.com/en/index.php?f=2222&exch=nasdaq&showcategories=STK&p=&cc=&limit=100&page={}'.format(page_idx))
    soup = BeautifulSoup(URL.text, 'html.parser')
    stocks_table = soup.find_all('table', class_ = 'table table-striped table-bordered')
    stocks_info = stocks_table[2]('td')
    for i, j in zip(range(0, 396, 4), range(1, 397, 4)):
        stocks_ticker = str(stocks_info[i])
        result_ticker = re.search('%s(.*)%s' % (start_ticker, end_ticker), stocks_ticker).group(1)
        tickers.append(result_ticker)
        stocks_name = str(stocks_info[j])
        result_name = re.search('%s(.*)%s' % (start_name, end_name), stocks_name).group(1)
        names.append(result_name)

    print('Extracting page', page_idx)

output = {}
for key in tickers:
    for value in names:
        output[key] = value
        names.remove(value)
        break

print(output)