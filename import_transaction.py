import pandas as pd
import numpy as np
import plotly.express as px               #to create interactive charts
import matplotlib.pyplot as plt

#to do: in and uit
# dashboard maken
# lender spender?

#https://towardsdatascience.com/manage-your-money-with-python-707579202203
#%%
# net worth on 1_10_2020 (start)
Mitch_01_10_2020_lopend = 384.53
Mitch_01_10_2020_spaar = 3590.61
Mitch_01_10_2020_degiro = 1000
Melissa_01_10_2020_lopend = 384.53 #onbekend
Melissa_01_10_2020_spaar = 3260.94

net_worth_1_10_2020_Mitch = Mitch_01_10_2020_lopend + Mitch_01_10_2020_spaar + Mitch_01_10_2020_degiro
net_worth_1_10_2020_Melissa = Melissa_01_10_2020_lopend + Mitch_01_10_2020_spaar

data = [['20/10', net_worth_1_10_2020_Mitch, 'Savingsaccount', 'Mitch'], ['20/10', net_worth_1_10_2020_Melissa, 'Savingsaccount', 'Melissa']]
net_worth_1_10_2020_together = pd.DataFrame(data, columns = ['year_month', 'Transactionamount', 'Category', 'Name'])

#%% load data
df_expenses_Mitch = pd.read_excel (r'/home/mitch/Documenten/Expenses/01-10-2020-01-01-2022.xls')
df_expenses_Melissa = pd.read_csv (r'/home/mitch/Documenten/Expenses/NL65INGB0001928665_01-10-2020_01-01-2022.csv')

#%% process data
df_expenses_Melissa['Bedrag (EUR)'] = df_expenses_Melissa['Bedrag (EUR)'].str.replace('[A-Za-z]', '').str.replace(',', '.').astype(float)
df_expenses_Mitch = df_expenses_Mitch.rename(columns={'Transactiedatum': 'Transactiondate','Transactiebedrag': 'Transactionamount'} )
df_expenses_Melissa = df_expenses_Melissa.rename(columns={'Datum': 'Transactiondate','Bedrag (EUR)': 'Transactionamount', 'Naam / Omschrijving': 'Omschrijving'} )
df_expenses_Melissa['Transactionamount'] = df_expenses_Melissa['Transactionamount'].astype(float)
df_expenses_Melissa['Transactionamount'][df_expenses_Melissa['Af Bij']=='Af'] = df_expenses_Melissa['Transactionamount'][df_expenses_Melissa['Af Bij']=='Af']*-1

#%% make categories

df_expenses_Mitch['Name'] = 'Mitch'
df_expenses_Mitch['Category'] = df_expenses_Mitch['Omschrijving']
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('Aldi|LIDL|AH|Albert Heijn|VOMAR|JUMBO|SPAR|Hoogvliet|VIS|Aardappel|Fruit|Bakkerij|V.O.F.|Van Bemmel|Brood&Ko|Groente|R. Bakker|Brasserie|Biefstro|Sushi|HELLOFRESH|TooGoodToGo|steversbanket|MCDONALD|mcd|takeaway|NUSA|sapori|ijssalon|Khop Khun Thai|CCVWoodstone|Food Ticket|Uber|maartens olijven|BUNSCHOTEN-SP|jansen|happy italy', case=False), 'Food', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('Wehkamp|Action|HEMA|HM|Zalando|Score|WE|BIG BAZAR|Intertoys|ETOS|Kruidvat|Wibra|Bol.com|BOLCOM|Haasbeek|Boekenvoordeel|GSMpunt|Bruna|Leen Bakker|Hennie Dost|Infomedics|ONLY|Nelson Schoenen|Tinka|BESTSELLER|Marktplaats|kringloop|rataplan|used products|Het Goed Geldrop|media markt|coolblue|prijsmepper|filiaal|apotheek|CCV DECOTREND|primera|Gezondheid aan huis|CCV Meijndert|maartens olijven|Bloemsierkunst',case=False), 'Living (non-food)', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('Simpel|Credit Card|OranjePakket|BasisPakket|Zilveren kruis|promovendum|NVVTG', case=False), 'Abbonements', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('tikkie|Spotify|Hardloopshop|thermen|reisreport|reisboekwinkel|Hairstyling|BrainWash|GiftFor2|Meneer Chocolade|Identity Servicescoffee|Foods|Koeien en Kaas|Noord Holland Catering|City Hall|Decathlon|VUMC Bedr.rest|Vermaat-VUMC|AMC deli|MANUELE THERAPIE|pathe|AAV|De Utrechter|Bibliotheek|Kaartje2Go|vinted|amazon|Maggie Blue|AKO|social deal|Perfect Marketing|bladkado|UMC UTRECHT|CCVChen|TicketingPayments|Gaston|oosterveer|C&M MARKET',case=False), 'Spare time', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('BELEG.|Beleggersgiro|Bitvavo|DIVIDEND|flatex', case=False), 'Investments', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('NL20ABNA0523679823', case=False), 'Savingsaccount', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('camping|fletcher|airbnb|booking|hotel|Land: BE|Land: AT|Land: SI|Land: DE|DE HAAN ZWAARDSLOOTERW|Rotisserie|CCV Eetcafe Minckelers|Geulhof Mechelen|Cafe Quanten|de zeute aardbei|LUNCHROOM|de Muldermolen|Nollen Borculo|De Herberg Vorden|Gelati e Panini|Beugelsdijk Food|Hoogervorst Horeca|CCVSLAGERIJ|De Kakelhof',case=False), 'Holiday', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('Geldmaat',case=False), 'Cash withdrawal', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('ICIN|blazhoffski', case=False), 'Income', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('MD van Gaalen', case=False), 'Together', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('PRAXIS|LB fil.|Karwei|Gamma|JYSK|Xenos|Etos|ONLY|Leen Bakker|Beter Bed|Beter bedbv|Toolstation|Intratuin|Bosrand|overvecht|J.w. van Gaalen|Gemeente|Energie|OASEN|WATERNET|T-Mobile|Belastingsamenw.|Regionale Belasting Groep|Belastingen|Fenor|volkskrant|AD NIEUWSMEDIA|ALGEMEEN DAGBLAD|DUWO|Keukeninbouwcenter|Allesvoorparket', case=False), 'House', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('NS groep|total|MULTI ENERGY|De Rolaf BV|Schaars Kaba|Tango|tinq|Argos|Tamoil|Formule 2|SHELL|ARAL|autohof|OV-Chipkaart|TOM|59-XJG-8|InShared|Kwikfit|Car Care|Q park|AVIA Xpress|ESSO|Parkeren|GVB voertuig|BP kerk|Park dak|Parkeergelden|P  DEN HAAG|AMSTERDAM RAI|P Amsterdamse Bos|Park Str Alphen|Betaald Park|CCVURW', case=False), 'Mobility', df_expenses_Mitch['Category'] )
df_expenses_Mitch['Category'] = np.where(df_expenses_Mitch['Category'].str.contains('Graaf|Boom|Betaalverzoek|Ideal|Overboeking|L.C. van Gaalen|M.R. Molenaar|AE van Gaalen|LA van Gaalen|Creditcard|Erasmus Universitair|Desk Services|CCVVereniging|CCVREKA|CCV ACADEMISCH ZIEKENH,', case=False), 'Diverse', df_expenses_Mitch['Category'] )


df_expenses_Melissa['Name'] = 'Melissa'
df_expenses_Melissa['Category'] = df_expenses_Melissa['Omschrijving']
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('Aldi|LIDL|AH|Albert Heijn|VOMAR|JUMBO|SPAR|Hoogvliet|VIS|Aardappel|Fruit|Bakkerij|V.O.F.|Van Bemmel|Brood&Ko|Groente|R. Bakker|Brasserie|Biefstro|Sushi|HELLOFRESH|TooGoodToGo|steversbanket|MCDONALD|mcd|takeaway|NUSA|sapori|ijssalon|Khop Khun Thai|CCVWoodstone|Food Ticket|Uber|maartens olijven|BUNSCHOTEN-SP|jansen|happy italy|CCVSLAGERIJ', case=False), 'Food', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('Wehkamp|Action|HEMA|HM|Zalando|Score|WE|BIG BAZAR|Intertoys|ETOS|Kruidvat|Wibra|Bol.com|BOLCOM|Haasbeek|Boekenvoordeel|GSMpunt|Bruna|Hennie Dost|Infomedics|ONLY|Nelson Schoenen|Tinka|BESTSELLER|Marktplaats|kringloop|rataplan|used products|Het Goed Geldrop|media markt|coolblue|prijsmepper|filiaal|apotheek|CCV DECOTREND|primera|Gezondheid aan huis|Bloemsierkunst',case=False), 'Living (non-food)', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('Simpel|Credit Card|OranjePakket|BasisPakket|Zilveren kruis|promovendum|NVVTG', case=False), 'Abbonements', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('tikkie|Spotify|M.R. Molenaar|Hardloopshop|thermen|Hotel|reisreport|reisboekwinkel|ABN AMRO Bank NV|Hairstyling|BrainWash|GiftFor2|Meneer Chocolade|A Wassenburg|Identity Services|coffee|Foods|Koeien en Kaas|Noord Holland Catering|City Hall|Decathlon|VUMC Bedr.rest|Vermaat-VUMC|MANUELE THERAPIE|pathe|De Utrechter|Bibliotheek|PinkGellac.nl|Kaartje2Go|vinted|amazon|MW L N vd Bosch|Maggie Blue|AKO|social deal|Perfect Marketing|bladkado|UMC UTRECHT|CCVChen|OCW - DUO|TicketingPayments|TECHNISCHE UNIVERSITEIT|BeansWKZ',case=False), 'Spare time', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('BELEG.|Beleggersgiro|Bitvavo|DIVIDEND|flatex', case=False), 'Investments', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('MD van Gaalen', case=False), 'Savingsaccount', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('camping|fletcher|airbnb|booking|hotel|Land: BE|Land: AT|Land: SI|Land: DE|DE HAAN ZWAARDSLOOTERW|Rotisserie|CCV Eetcafe Minckelers|Geulhof Mechelen|Cafe Quanten|de zeute aardbei|LUNCHROOM|de Muldermolen|Nollen Borculo|De Herberg Vorden|Gelati e Panini|Beugelsdijk Food|Hoogervorst Horeca|De Kakelhof|bled',case=False), 'Holiday', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('Geldmaat',case=False), 'Cash withdrawal', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('JMC Management|UNIVERSITAIR MEDISCH CENTRUM UTRECHT', case=False), 'Income', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('Mitchel Molenaar|M.A. Molenaar', case=False), 'Together', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('PRAXIS|Karwei|Gamma|JYSK|Xenos|LB fil.|Leen Bakker|Beter Bed|Beter bedbv|Toolstation|Intratuin|Bosrand|overvecht|J.w. van Gaalen|Gemeente|Energie|OASEN|WATERNET|T-Mobile|Belastingsamenw.|Regionale Belasting Groep|Belastingen|Fenor|volkskrant|AD NIEUWSMEDIA|ALGEMEEN DAGBLAD|DUWO|Keukeninbouwcenter|DC03|Allesvoorparket', case=False), 'House', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('NS groep|total|MULTI ENERGY|De Rolaf BV|Schaars Kaba|Tango|tinq|Argos|Tamoil|Formule 2|SHELL|ARAL|autohof|OV-Chipkaart|TOM|59-XJG-8|InShared|Kwikfit|Car Care|Q park|AVIA Xpress|ESSO|Parkeren|GVB voertuig|BP kerk|Park dak|Parkeergelden|P  DEN HAAG|AMSTERDAM RAI|P Amsterdamse Bos|Park Str Alphen|Betaald Park|CCVURW', case=False), 'Mobility', df_expenses_Melissa['Category'] )
df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('Graaf|Boom|Betaalverzoek|Ideal|Overboeking|L.C. van Gaalen|AE van Gaalen|LA van Gaalen|Creditcard|Erasmus Universitair|Desk Services|CCVVereniging|CCVREKA', case=False), 'Diverse', df_expenses_Melissa['Category'] )



#df_expenses_Melissa['Category'] = np.where(df_expenses_Melissa['Category'].str.contains('nan', case=False), 'Diverse', df_expenses_Melissa['Category'] ) # deze weghalen als je categorien wilt aanpassen

#%% data per month
df_expenses_Mitch['year_month'] = pd.to_datetime(df_expenses_Mitch['Transactiondate'].astype(str), format='%Y%m%d')
df_expenses_Mitch['year_month']  = df_expenses_Mitch['year_month'].dt.strftime("%y/%m")
df_expenses_Melissa['year_month'] = pd.to_datetime(df_expenses_Melissa['Transactiondate'].astype(str), format='%Y%m%d')
df_expenses_Melissa['year_month']  = df_expenses_Melissa['year_month'].dt.strftime("%y/%m")

#%% expenses and plots
# all expenses
df_together = pd.concat([df_expenses_Melissa[['year_month', 'Transactionamount', 'Category', 'Name']], df_expenses_Mitch[['year_month', 'Transactionamount', 'Category', 'Name']]])

# expenses both
Expenses_Mitch = df_expenses_Mitch[(df_expenses_Mitch.Category != "Income") & (df_expenses_Mitch.Category != "Spare time") & (df_expenses_Mitch.Category != "Savingsaccount") & (df_expenses_Mitch.Category != "Investments") ] 
Expenses_Melissa = df_expenses_Melissa[(df_expenses_Melissa.Category != "Income") & (df_expenses_Melissa.Category != "Spare time") & (df_expenses_Melissa.Category != "Savingsaccount") & (df_expenses_Melissa.Category != "Investments") ] 

#net expenses in table
Net_expenses_Mitch = Expenses_Mitch.groupby('year_month')['Transactionamount'].sum().reset_index(name ='sum_Mitch')
Net_expenses_Melissa = Expenses_Melissa.groupby('year_month')['Transactionamount'].sum().reset_index(name ='sum_Melissa')
Net_expenses_together = Net_expenses_Mitch.merge(Net_expenses_Melissa, on='year_month', how='outer')
Net_expenses_together['Mitch_earns'] = (Net_expenses_together['sum_Mitch'] - Net_expenses_together['sum_Melissa'])*-1
Net_expenses_together['Mitch_earns_cumulative'] = Net_expenses_together['Mitch_earns'].cumsum() # bedrag rechtsonder is bedrag dat het verschil is tussen uitgaven tussen mitch en melissa. Dit getal gedeeld door 2 moet de een aan de ander betalen. 

print('Mitch earns from Melissa', Net_expenses_together.iloc[len(Net_expenses_together)-1]['Mitch_earns_cumulative'])

# total savings and investments
df_savings = df_together[(df_together.Category == "Savingsaccount") | (df_together.Category == "Investments") ]
df_savings['Transactionamount'] = df_savings['Transactionamount']*-1
df_savings = df_savings.append(net_worth_1_10_2020_together) # append data at start

Net_Worth_Table= df_savings.groupby('year_month')['Transactionamount'].sum().reset_index(name ='sum')
Net_Worth_Table['cumulative sum'] = Net_Worth_Table['sum'].cumsum()
# plot total savings and investments
plt.figure(0)
plt.plot(Net_Worth_Table['year_month'], Net_Worth_Table["cumulative sum"])
plt.title("Net Worth Over Time")
plt.xlabel('Net Worth Over Time') 
plt.ylabel('Net Worth') 
plt.show()

# total expenses without savings and investments
df_expenses = df_together[(df_together.Category != "Savingsaccount") & (df_together.Category != "Investments") ]
df_expenses['Transactionamount'] = df_expenses['Transactionamount']*-1
# plot total expenses
plt.figure(1)
Total_Monthly_Expenses_Table = df_expenses.groupby('year_month')['Transactionamount'].sum().reset_index(name = 'sum')
Total_Monthly_Expenses_Chart = px.bar(Total_Monthly_Expenses_Table, x = "year_month", y = "sum", title = "Total Monthly Expenses")
plt.bar(Total_Monthly_Expenses_Table['year_month'], Total_Monthly_Expenses_Table['sum'])
plt.title("Expenses Over Time")
plt.xlabel('Expenses Over Time') 
plt.ylabel('Expenses') 

