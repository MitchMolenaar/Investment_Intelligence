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

def simple_dashboard(your_xls_file):
    """
    Parameters
    your_xls_file : type = STRING
        r'C:\your\path\to\your\degiro\export\filename.xls'

    Returns
    Simple graph of your shares in De Giro, GAK and total money invested
    Pandas DataFrame calles 'total' with all transaction in it
    
    """
    #import your exported .xls file and call it trans.
    #insert your own personal paht to your xls file:
    trans = pd.read_excel (your_xls_file)

    #remove all rows which does not include an Order Id:
    trans.dropna(subset=['Order Id'], inplace=True)

    #rename columns:
    trans.columns = ['date', 'del0', 'del1', 'product', 'ISIN', 'description',
                     'del2', 'valuta', 'value', 'del3', 'del4', 'del5']

    #remove colums which are unnecesary (named 'del#'):
    trans = trans[trans.columns[~trans.columns.str.contains('del')]]
    trans = trans.reset_index() #reset indices

    #extract number of products bought, price per product, products bought and their initial value
    trans_des = trans["description"].str.split(" ", n = -1, expand = True)
    num_products = trans_des[1]
    pric_pp = trans_des[3]
    products = trans["product"]
    ISIN = trans["ISIN"]
    values = trans["value"]

    #combine products in one dataframe
    global total #global makes it possible to return variable
    total = pd.concat([products, ISIN, num_products, pric_pp, values], axis=1) 
    total.columns=["product", "isin", "number", "ini_value", "total_value"]

    #creating subplots
    fig = plt.figure(figsize=(10,5))
    sub1 = fig.add_subplot(131)
    sub2 = fig.add_subplot(132)
    sub3 = fig.add_subplot(133)

    #plot the data and set lables
    sub1.barh(total["isin"], total["number"]) #number of shares
    sub2.barh(total["isin"], total["ini_value"]) #mean purchase value
    sub3.barh(total["isin"], total["total_value"]*(-1)) #total money invested
    sub1.set_xlabel('# of shares')
    sub2.set_xlabel('GAK (€)')
    sub2.axes.get_yaxis().set_visible(False) #hide ylabel
    sub2.set_title('Overview of De Giro portfolio')
    sub3.set_xlabel('Total invested (€)')
    sub3.axes.get_yaxis().set_visible(False) #hide ylabel
    
    return total

#run simple_dashboard function
simple_dashboard(r'C:\Users\ttmoo\Documents\Administratie\Privé\Github\Account.xls')

#testdf = total[total['isin'].isin(total['isin'].value_counts()[total['isin'].value_counts()>1].index)]
#total.groupby(['isin']).get_group('NL0009690221')