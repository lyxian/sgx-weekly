import pandas
import os

DIR = 'data'

def readFile(filename):
    extn = filename.split('.')[-1]
    if extn == 'csv':
        return pandas.read_csv(f'{DIR}/{filename}')
    elif extn == 'json':
        pass 
    else:
        raise Exception('Data file type not supported')

def getFileNameAndData():
    FILENAME = [filename for filename in os.listdir(DIR) if 'Grouped' in filename][0]
    return FILENAME, readFile(FILENAME)

def getMinMaxDf():
    from postWeekly import masterDf, TICKERS

    STATS = ['min', 'max']
    rangeDf = pandas.DataFrame()
    for ticker in TICKERS:
        tmpDf = masterDf.loc[masterDf.ticker == ticker, ['close']].describe().loc[STATS]
        tmpDf.columns = [ticker]
        rangeDf = pandas.concat([rangeDf, tmpDf], axis=1)

    return rangeDf