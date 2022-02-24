import pendulum
import requests
import pandas
import json
import re

class yfDataReader():
    def __init__(self):
        self.url = 'https://sg.finance.yahoo.com/quote/{}/history'
        self.params = {
            'filter': 'history',
            'interval': '1d',
            'frequency': '1d'
        }
        self.headers = {
            "Connection": "keep-alive",
            "Expires": str(-1),
            "Upgrade-Insecure-Requests": str(1),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def getTickerPriceDf(self, ticker, startDate=pendulum.datetime(2020,1,1,tz='Asia/Singapore'), endDate=pendulum.today()):
        if not isinstance(startDate, pendulum.DateTime) or not isinstance(endDate, pendulum.DateTime):
            raise Exception('Start/End date has bad data type, please use DateTime objects')
        else:
            startDate = int(startDate.timestamp())
            endDate = int(endDate.timestamp())

        tickerUrl = self.url.format(ticker)
        tickerParams = {
            'period1': startDate,
            'period2': endDate,
            **self.params
        }

        print(f'Getting response from {tickerUrl}')
        response = requests.get(url=tickerUrl, params=tickerParams, headers=self.headers)
        data = json.loads(re.search(r'root\.App\.main = (.*?);\n}\(this\)\);', response.text).group(1))["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]
        prices = [i for i in data['prices'] if 'type' not in i.keys()]
        # with open('x.json', 'w') as file:
        #     file.write(json.dumps(data, indent=4))

        df = pandas.DataFrame(prices).sort_values(by=['date'], ascending=True)
        df.loc[:, 'date'] = df['date'].apply(lambda x: pendulum.from_timestamp(x).to_date_string())
        df = df.set_index("date")

        return df

    def getTickerPriceDfs(self, tickers, startDate, endDate):
        dfs = [self.getTickerPriceDf(ticker, startDate, endDate) for ticker in tickers]

        return pandas.concat(dfs, keys=tickers, names=['ticker','date'])
