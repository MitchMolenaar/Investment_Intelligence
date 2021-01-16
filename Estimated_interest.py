# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 18:45:20 2021

@author: mitch
"""


monthly_invest = 1000 #How many money each month
principal = 100 # current euros in degiro
years = 30 # years of saving
monthly_invest = monthly_invest*12
interest = 0.05 # intest in decimal numbers.

final_amount = 0

total_capital = []
total_dividend = []

for i in range(0, years):
    if final_amount == 0 :
        final_amount = principal
    final_amount = (final_amount + monthly_invest) * (1+interest)
    
    total_capital.append(monthly_invest)
    total_capital1=sum(total_capital)
    
    #total_dividend.append((final_amount + monthly_invest) * interest)
    #total_capital.append(monthly_invest)
    #total_interest.append((final_amount + monthly_invest)*interest)
    #total_capital.append(monthly_invest*i)
    #total_dividend.append(final_amount-total_capital[i])    
    print('after', i+1,  'years you have', int(final_amount), 'euro with', total_capital1+principal, 'euro capital, dividend total = ', int(final_amount)-(total_capital1+principal), 'euro')
print('total capital = ', (monthly_invest*years)+principal)
print('total dividend = ', final_amount-((monthly_invest*years)+principal))