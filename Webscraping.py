# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 17:11:50 2020

@author: mitch

To do: 
- algemene input maken zodat iedereen in de folder dit script kan runnen

"""

# https://codingandfun.com/scrape-yahoo-finance-using-python/



import numpy as np 
import pandas_datareader as web 
from datetime import datetime 
# To visualize the results 
import matplotlib.pyplot as plt 
import seaborn

import pandas as pd
import csv
import ssl
import socket
import smtplib


# Interesting companies
companies = [['IBM','Technology'],['DLR','Real Estate'], ['LTC','Real Estate'], ['ABT','Health Care'], 
             ['UL','Consumer Staples'], ['T', 'Communication Services'], ['NEDAP.AS', 'Technology'], ['NSRGY','Consumer Staples'],
             ['PFE','Health Care'], ['GLPG.AS', 'Health Care'], ['PHIA.AS','Health Care'], ['GOOG','Health care'], ['DIS', 'Fun'],
             ['FSLY','Technology'], ['Alfen.AS','Energy'], ['AMZN','Combi'], ['JNJ','Health Care']] # ['GILD','Health Care']

# Abbreviations and start date 
symbols=[]
start = datetime(2012, 1, 1)
symbols_list = ['IBM', 'T', 'LTC', 'PFE', 'JNJ']



########################################################################################################################################
df=pd.DataFrame();
for company in companies:
    print(company)
    statistics = pd.read_html(f'https://finance.yahoo.com/quote/{company[0]}/key-statistics?p={company[0]}');
    statistics2 = pd.read_html(f'https://finance.yahoo.com/quote/{company[0]}?p={company[0]}');
    prices = statistics2[0];
    summary = statistics2[1];
    valuation_Measures = statistics[0];
    stock_Price_History = statistics[1];
    share_Statistics = statistics[2];
    dividend_Info = statistics[3];
    profitability_Info = statistics[5];
    management_Efectiveness = statistics[6];
    income_Statement = statistics[7];
    balance_Sheet = statistics[8];
    ###cash_Flow = statistics[9];
    df1=pd.DataFrame({"Stock":[company[0]],
                      "Sector":[company[1]],
                      "Close_price":[prices[1][0]],
                      "50-day_moving average":[stock_Price_History[1][5]],
                      "200-day_moving average":[stock_Price_History[1][6]],
                      "P/E_ratio":[summary[1][2]],
                      "Earning_per_share":[summary[1][3]],
                      "Forward_annual_dividend_yield":[dividend_Info[1][1]],
                      "Trailing_annual_dividend_yield":[dividend_Info[1][3]],
                      "Trailing_annual_dividend_rate":[dividend_Info[1][2]],
                      "5_year_average_dividend_yield":[dividend_Info[1][4]],
                      "Payout_ratio":[dividend_Info[1][5]],
                      "Revenue_per_share":[income_Statement[1][1]],
                      "Return_on_equity":[management_Efectiveness[1][1]],
                      #return on assests
                      #profatibility_info
                      "Total_cash_per_share":[balance_Sheet[1][1]],
                      "Total_debt":[balance_Sheet[1][2]],
                      ###"Operating_cash_flow":[cash_Flow[1][0]],
                      # levered free cash flow
                      "Short % of shares outstanding":[share_Statistics[1][9]],
                      });
    df=df.append(df1); #append dataframe
    
df=df.reset_index(drop=True)

# dataframe to floats
df['Close_price'] = df['Close_price'].astype('float')
df['50-day_moving average'] = df['50-day_moving average'].astype('float')
df['200-day_moving average'] = df['200-day_moving average'].astype('float')
df['P/E_ratio'] = df['P/E_ratio'].astype('float')
df['Earning_per_share'] = df['Earning_per_share'].astype('float')
df['Revenue_per_share'] = df['Revenue_per_share'].astype('float')
df['5_year_average_dividend_yield'] = df['5_year_average_dividend_yield'].astype('float')
df['Total_cash_per_share'] = df['Total_cash_per_share'].astype('float')
#df['Total_cash_per_share'] = df['Total_cash_per_share'].astype('float')
df['Trailing_annual_dividend_yield'] = df['Trailing_annual_dividend_yield'].str.rstrip('%').astype('float')
df['Forward_annual_dividend_yield'] = df['Forward_annual_dividend_yield'].str.rstrip('%').astype('float')
df['Payout_ratio'] = df['Payout_ratio'].str.rstrip('%').astype('float')
df['Return_on_equity'] = df['Return_on_equity'].str.rstrip('%').astype('float')
df['Short % of shares outstanding'] = df['Short % of shares outstanding'].str.rstrip('%').astype('float')

df=df.sort_values(by=['P/E_ratio'], ascending=False)

df.to_csv (r'C:\Users\mitch\anaconda3\Stocks\finance_sc\Stocks.csv', index = False, header=True)       #save dataframe to csv

#Analysis = pd.read_csv(r'C:\Users\mitch\anaconda3\Stocks\finance_sc\Stocks.csv')  # Read in the ranked stocks

########################################################################################################################################
###Make covariation matrix to see dependence of stocks in the past ###
for ticker in symbols_list:     
    r = web.DataReader(ticker, 'yahoo', start)   
    # add a symbol column   
    r['Symbol'] = ticker    
    symbols.append(r)
# concatenate into df
df1=df
df1 = pd.concat(symbols)
df1 = df1.reset_index()
df1 = df1[['Date', 'Close', 'Symbol']]
df1.head()
df_pivot=df1.pivot('Date','Symbol','Close').reset_index()
df_pivot.head()

corr_df = df_pivot.corr(method='pearson')
#reset symbol as index (rather than 0-X)
corr_df.head().reset_index()
#del corr_df.index.name
corr_df.head(10)

plt.figure(figsize=(13, 8))
seaborn.heatmap(corr_df, annot=True, cmap="YlGnBu")
plt.figure()