# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:32:44 2021

This file can be used to import an overview of your transactions

Goal: Automatically read all transactions and calculate current portfolio, including:
    Number of effects
    GAK
    Transaction costs
    Dividend income
    
Before running, insert in anaconda:
pip install --user currencyconverter

To do:
    - winst bereken: huidige waarde aandeel - aankoop waarde
Lopend:
    - wisselkoersen toevoegen bij kopen aandeel buitenlandse markt.  De currency converter is niet accuraat --> andere scraper

"""
#imports
import pandas as pd
import matplotlib.pyplot as plt
import csv
from currency_converter import CurrencyConverter


"""
Parameters
your_csv_file : type = STRING
    r'C:\your\path\to\your\degiro\export\filename.csv'

Returns
Simple graph of your shares in De Giro, GAK and total money invested
Pandas DataFrame calles 'total' with all transaction in it

"""

def simple_dashboard(your_csv_file_transactions, your_csv_file_account, companies):
#import your exported .csv files and call them Transactions and Account.
#insert your own personal paths to your files:
#simpledashboard(your_csv_file_transactions,your_csv_file_account)
#import your stocks/companies as shown below. THe abbreviations are from Yahoo finance.
    transaction =  pd.read_csv(your_csv_file_transactions) 
    account = pd.read_csv(your_csv_file_account)
    
    #remove all rows which does include an Order Id:
    #transaction.drop(['Order ID'], axis=1, inplace=True)
    #account.drop(['Order Id'], axis=1, inplace=True)
    


    #make dataframe portfolio
    portfolio=[]
    list_of_stocks = transaction.Product.unique() #all names of stocks in portfolio in the past
    for stock in list_of_stocks:   #iterate over the different stocks.
        specific_stock = transaction[transaction['Product'] == stock] #pick one stock of the ones in your portfolio
        Total_number_specific_stock = sum(specific_stock.Aantal) # summate all totals of that stock (so bought minus sold)
        Total_value_specific_stock = sum(specific_stock.Totaal) # summate the total vallue of that stock
        Sold_value = sum(specific_stock.Totaal[specific_stock.Totaal >= 0])  #summate for how much you have sold the stocks
        Bought_value = sum(specific_stock.Totaal[specific_stock.Totaal < 0]) #summate for how much you have bought the stocks
        Stock_in_portfolio=pd.DataFrame({'Stock': [stock], 'Current number of stocks':[Total_number_specific_stock],
                                         'Bought (€)':[Bought_value], 'Sold (€)':[Sold_value],
                                         'Difference bought/sold (€)':[Total_value_specific_stock]}) #put values in dataframe
        portfolio.append(Stock_in_portfolio) # append the data of all stocks
        print(stock)
        
    comp=pd.DataFrame(); # make a dataframe for companies
    for company in companies: #iterate over the companies
        print(company)
        statistics = pd.read_html(f'https://finance.yahoo.com/quote/{company[0]}/key-statistics?p={company[0]}'); #read statistics from yahoo finance
        statistics2 = pd.read_html(f'https://finance.yahoo.com/quote/{company[0]}?p={company[0]}'); #read statistics from yahoo finance
        prices = statistics2[0]; #extract prices from yahoo finance
        summary = statistics2[1]; # extract data from tab summary in yahoo finance
        comp1=pd.DataFrame({"Stock":[company[1]], 
                          "Stock_abr":[company[0]],
                          "Sector":[company[2]],
                          "Close_price":[prices[1][0]],
                          "Valuta":[(company[3])]
                          }); # make dataframe with the stock, the abbreviation of the stock, the sector and the close price.
        comp=comp.append(comp1); #append dataframe for each stock
    comp = comp.set_index('Stock') # set index as stock name   
    comp['Close_price']=comp['Close_price'].astype(str).astype(float) # transform close price to a float/number.
    
    # transform valuta to euro
    c = CurrencyConverter()
    comp.loc[comp['Valuta'] == 'USD', 'Close_price'] = c.convert(comp.loc[comp['Valuta'] == 'USD', 'Close_price'], 'USD', 'EUR')
    comp.Valuta= 'Euro' # make valuta column 'euro' now.
    
    portfolio = pd.concat(portfolio) # put all stocks in one dataframe
    portfolio = portfolio.set_index('Stock') # set index as stock name
    portfolio = portfolio.join(comp)
    portfolio['Current value Stock'] = portfolio['Close_price'] * portfolio['Current number of stocks']
    
    #creating subplots
    fig = plt.figure(figsize=(10,5))
    sub1 = fig.add_subplot(131)
    sub2 = fig.add_subplot(132)
    sub3 = fig.add_subplot(133)

    #plot the data and set lables
    sub1.barh(portfolio.index, portfolio["Current number of stocks"], height=0.75) #number of shares
    sub2.barh(portfolio.index, (portfolio["Difference bought/sold (€)"]*(-1)/portfolio["Current number of stocks"]), height=0.75) #mean purchase value
    sub3.barh(portfolio.index, portfolio["Difference bought/sold (€)"]*(-1), height=0.75) #total money invested
    sub1.set_xlabel('# of stocks')
    sub2.set_xlabel('GAK (€)')
    sub2.axes.get_yaxis().set_visible(False) #hide ylabel
    sub2.set_title('Overview of De Giro portfolio')
    sub3.set_xlabel('Total invested (€)')
    sub3.axes.get_yaxis().set_visible(False) #hide ylabel
    
    portfolio = portfolio[['Stock_abr','Sector','Current number of stocks','Bought (€)', 'Sold (€)', 'Difference bought/sold (€)', 'Close_price', 'Current value Stock']]  # change order of columns
    
    return portfolio, comp, transaction




check_portfolio_of='Mitch' ## fill in name of person

if check_portfolio_of=='Timo':
    companies = [['PHARM.AS', 'PHARMING GROUP', 'Health care']]
    [portfolio,comp, transaction]=simple_dashboard(r'C:\Users\ttmoo\Documents\Administratie\Privé\Github\Transactions.csv',
                           r'C:\Users\ttmoo\Documents\Administratie\Privé\Github\Account.csv', companies)


if check_portfolio_of=='Mitch':
    companies = [['IBM', 'INTERNATIONAL BUSINESS', 'Technology', 'USD'], # fill in: abbrevaiation (yahoo finance), company, sector, and which valuta you have bought the stock
                 ['GLPG.AS', 'GALAPAGOS', 'Health Care', 'EURO'], 
                 ['IEUR', 'ISHARES MSCI EUR A', 'ETF', 'EURO'], 
                 ['RDSA.AS', 'ROYAL DUTCH SHELLA', 'Energy', 'EURO'],
                 ['PHARM.AS', 'PHARMING GROUP', 'Health care', 'EURO'],
                 ['GOOG', 'ALPHABET INC. - CLASS A', 'Technology', 'EURO'],
                 ['ASML.AS', 'ASML HOLDING', 'Technology', 'EURO'],
                 ['DSM.AS', 'DSM KON', 'Technology', 'EURO']]
    
    [portfolio,comp, transaction]=simple_dashboard(r'C:\Users\mitch\Documents\GitHub\Investment_Intelligence\Transactions.csv',
                           r'C:\Users\mitch\Documents\GitHub\Investment_Intelligence\Account.csv', companies)
               
          

