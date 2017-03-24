from yahoo_finance import * 
import xlwt
import csv
import numpy as np


slist = ['WMT','JNJ','MMM', 'UTX', 'PG', 'PFE', 'VZ', 'MSFT', 'KO','MRK', 'INTC', 'TRV', 'HD', 'GE', 'BA', 'AXP', 'GS', 'NKE', 'DIS', 'AAPL', 'UNH', 'V', 'CSCO', 'IBM', 'DD', 'XOM', 'JPM', 'CVX', 'CAT', 'MCD']
op = []
cl = []
stock_names = []

for s in slist:
    stock=Share(s);
    values = stock.get_historical('2017-03-22','2017-03-22')
    op.append(float(values[0]["Open"]))
    cl.append(float(values[0]["Adj_Close"]))

diff = [i - j for i, j in zip(cl, op)]
diff_temp = sorted(diff)

for i in range(30):
    if(np.isclose(diff[i],diff_temp[0],rtol=1e-10, atol=1e-10)):
        min1 = i
    elif(np.isclose(diff[i],diff_temp[1],rtol=1e-10, atol=1e-10)):
        min2 = i
    elif(np.isclose(diff[i],diff_temp[28],rtol=1e-10, atol=1e-10)):
        max2 = i
    elif(np.isclose(diff[i],diff_temp[29],rtol=1e-10, atol=1e-10)):
        max1 = i
    else:
        pass
lst = [slist[max1],slist[max2],slist[min1],slist[min2]]
print(lst)