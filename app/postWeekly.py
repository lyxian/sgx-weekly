from utils import DIR
import pandas
import numpy

combinedDf = pandas.read_csv(f'{DIR}/stockPrices.csv').set_index('date')
TICKERS = numpy.unique([i.split('_')[0] for i in combinedDf.columns if i != 'date'])

# Transform Columns to Rows
if 0:
    desiredColumn = 'close'
    newDf = combinedDf.reset_index().melt(id_vars=['date'], var_name='ticker', value_name=desiredColumn,
        value_vars=[i for i in combinedDf if desiredColumn in i]) # params = ignore_index, col_level
    # Set index to date, Split ticker column 

masterDf = pandas.DataFrame()
for ticker in TICKERS:
    tmpDf = combinedDf.filter(regex=ticker).copy()
    tmpDf.columns = [i.split('_')[1] for i in tmpDf.columns]
    tmpDf.loc[:, 'ticker'] = tmpDf.iloc[:, 0].apply(lambda x: ticker)
    masterDf = pandas.concat([masterDf, tmpDf])

masterDf = masterDf.round(3)
# print(masterDf)
masterDf.loc[:, ['ticker', *masterDf.columns[:-1]]].to_csv('data/stockPricesGrouped.csv')

# Describe stock prices (min, max)
STATS = ['min', 'max']
rangeDf = pandas.DataFrame()
for ticker in TICKERS:
    tmpDf = masterDf.loc[masterDf.ticker == ticker, ['close']].describe().loc[STATS]
    tmpDf.columns = [ticker]
    rangeDf = pandas.concat([rangeDf, tmpDf], axis=1)

print(rangeDf)