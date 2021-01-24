# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:32:44 2021

This file can be used to import an overview of your transactions

Goal: Automatically read all transactions and calculate current portfolio, including:
    Number of effects
    GAK
    Transaction costs
    Dividend income

"""
#imports
import pandas as pd
import matplotlib.pyplot as plt
import csv

"""
Parameters
your_csv_file : type = STRING
    r'C:\your\path\to\your\degiro\export\filename.csv'

Returns
Simple graph of your shares in De Giro, GAK and total money invested
Pandas DataFrame calles 'total' with all transaction in it

"""

def simple_dashboard(your_csv_file_transactions, your_csv_file_account):
#import your exported .csv file and call it Transactions.
#insert your own personal path to your Transactions file:
#simpledashboard(your_csv_file_transactions,your_csv_file_account)
    transaction =  pd.read_csv(your_csv_file_transactions) 
    account = pd.read_csv(your_csv_file_account)
    
    #remove all rows which does include an Order Id:
    transaction.drop(['Order ID'], axis=1, inplace=True)
    account.drop(['Order Id'], axis=1, inplace=True)

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
                                         'Value of stocks':[Total_value_specific_stock], 'Bought':[Bought_value], 'Sold':[Sold_value]}) #put values in dataframe
        portfolio.append(Stock_in_portfolio) # append the data of all stocks
        print(stock)
    
    portfolio = pd.concat(portfolio) # put all stocks in one dataframe
    portfolio = portfolio.set_index('Stock') # set index as stock name
    
    return portfolio

portfolio=simple_dashboard(r'C:\Users\mitch\Documents\GitHub\Investment_Intelligence\Transactions.csv', r'C:\Users\mitch\Documents\GitHub\Investment_Intelligence\account.csv')

