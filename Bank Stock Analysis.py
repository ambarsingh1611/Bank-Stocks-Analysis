# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:18:47 2019

@author: Cosmic Dust
"""

from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

start = datetime.datetime(2006,1,1)
end = datetime.datetime(2019,1,1)

# Bank of America
BAC = data.DataReader('BAC', 'google', start, end)
# CitiGroup
C = data.DataReader('C', 'google', start, end)
# Goldman Sachs
GS = data.DataReader('GS', 'google', start, end)
# JPMorgan Chase
JPM = data.DataReader('JPM', 'google', start, end)
# Morgan Stanley
MS = data.DataReader('MS', 'google', start, end)
# Wells Fargo
WFC = data.DataReader('WFC', 'google', start, end)


""""""
# DataReader is deprecated, so I updated the code to munually load financial data
# from Yahoo Finance. Updated code below...
""""""

import os

os.chdir('C:/Users/CosmicDust/Downloads/Bank Stock Analysis')

BAC = pd.read_csv('BAC.csv')
C = pd.read_csv('C.csv')
GS = pd.read_csv('GS.csv')
JPM = pd.read_csv('JPM.csv')
MS = pd.read_csv('MS.csv')
WFC = pd.read_csv('WFC.csv')

BAC.set_index('Date', inplace=True)
C.set_index('Date', inplace=True)
GS.set_index('Date', inplace=True)
JPM.set_index('Date', inplace=True)
MS.set_index('Date', inplace=True)
WFC.set_index('Date', inplace=True)


tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

bank_stocks = pd.concat([BAC,C,GS,JPM,MS,WFC],axis=1,keys=tickers)
bank_stocks.head()

bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']
bank_stocks.head()


#----------------------------------EDA-----------------------------------------

# Max close price for each bank's stock throughout the time period
bank_stocks.xs(key='Close',axis=1, level='Stock Info').max()


returns = pd.DataFrame()

# NEW FEATURE
# Store the percent change of close price for each bank stock in returns DataFrame

for tick in tickers:
    returns[tick + ' Return'] = bank_stocks[tick]['Close'].pct_change()

returns.head()
returns.drop('2004-01-02', inplace=True)

sns.pairplot(returns)

returns.idxmin()
returns.idxmax()

returns.std()
returns.ix['2015-01-01':'2016-01-01'].std()

sns.distplot(returns.ix['2015-01-01':'2016-01-01']['MS Return'], color='green', bins=100)
sns.distplot(returns.ix['2008-01-01':'2009-01-01']['C Return'], color='red', bins=100)

# Line plot for Stocks closing price
for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,6),label=tick)
plt.legend()

# Moving Average to see the trend
plt.figure(figsize=(12,6))
C['Close'].ix['2007-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
C['Close'].ix['2007-01-01':'2009-01-01'].plot(label='C CLOSE')
plt.legend()

# Heatmap of closing price of stocks
sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(), annot=True)

# Heatmap of closing price during stock market crash
sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').ix['2007-01-01':'2009-01-01'].corr(), annot=True)

