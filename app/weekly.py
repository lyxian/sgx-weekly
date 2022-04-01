from dataReader import yfDataReader
from bs4 import BeautifulSoup
import pendulum
import requests
import pandas
import os 
import re

# COLUMNS = ['']
FILENAME = 'weekly.html'
reader = yfDataReader()
end = pendulum.today()
start = end.subtract(days=450)
# start = end.subtract(days=30)

if FILENAME not in os.listdir():
    url = 'https://sginvestors.io/market/sgx-weekly-top-turnover-institutions-retailers-buy-sell/'
    response = requests.get(url)
    with open('weekly.html', 'w') as file:
        file.write(response.text)
    content = response.text
else:
    with open('weekly.html', 'r') as file:
        content = file.read()

soup = BeautifulSoup(content, 'html.parser')

if 1:
    weeklyStocks = soup.find_all('tr', {'class': 'weekly-stock'})
else:
    if 1:
        with open('stocks', 'r') as file:
            weeklyStocks = file.read().strip().split('\n')
    else:
        #                                 *       *       *
        weeklyStocks = ['K71U', 'JYEU', 'J91U', 'CWBU', 'RW0U']

if 'stockPrices.csv' not in os.listdir('data'):
    data = {}
    # <company> (SGX:<ticker>)SGX:<ticker>
    for stock in weeklyStocks:
        try:
            stockText = stock.find_all('span')[0].text
            company, ticker = re.search(r'(.*) \(.*\)SGX:(.*)', stockText).groups()
        except Exception as e:
            ticker = stock 

        # data[company] = ticker
        # print(f'{company}:{ticker}')
        df = reader.getTickerPriceDf(f'{ticker}.SI', start, end)
        df = df.add_prefix(f'{ticker}_')
        # print(df)
        
        data[ticker] = df
        # break

    combinedDf = pandas.concat(data.values(), axis=1)
    combinedDf.to_csv('data/stockPrices.csv')
    # print(data)