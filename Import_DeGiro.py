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
import pandas as pd #import pandas to import excel file into pyhton

#import your exported .xls file and call it trans.
#insert your own personal paht to your xls file:
trans = pd.read_excel (r'C:\Users\ttmoo\Documents\Administratie\Privé\Github\Account.xls')

#remove all rows which does not include an Order Id:
trans.dropna(subset=['Order Id'], inplace=True)

#rename columns:
trans.columns = ['date', 'del0', 'del1', 'product', 'ISIN', 'description',
              'del2', 'valuta', 'value', 'del3', 'del4', 'del5']

#remove colums which are unnecesary (named 'del#'):
trans = trans[trans.columns[~trans.columns.str.contains('del')]]
trans = trans.reset_index() #reset indices
trans["description"]= trans["description"].str.split(" ", n = 2, expand = False) 

# iterate through each row and select  
# 'Name' and 'Age' column respectively. 
for i in range(len(trans)) : 
    print(trans.loc[i, "product"], trans.loc[i, "description"], trans.loc[i, "value"])
    products = trans["product"]
    num_products = trans["description"]
    values = trans["value"]*(-1)
