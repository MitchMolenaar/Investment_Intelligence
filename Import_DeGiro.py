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
trans = pd.read_excel (r'Your\path\to\your\xls\file\filename.xls')

#remove all rows which does not include an Order Id:
trans.dropna(subset=['Order Id'], inplace=True)

#rename columns:
trans.columns = ['date', 'del0', 'del1', 'product', 'ISIN', 'description',
              'del2', 'valuta', 'value', 'del3', 'del4', 'del5']

#remove colums which are unnecesary (named 'del#'):
trans = trans[trans.columns[~trans.columns.str.contains('del')]]

print(trans)
