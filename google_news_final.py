from bs4 import BeautifulSoup
import requests
import xlwt
import csv
import requests
import numpy as np
import pandas as pd
from newspaper import Article, Source
import datetime
import re

url = []
lst = np.arange(100,200,100)
print(lst)
names = []
dates = []
title = []
newspapers = []
slist = ['WMT','JNJ','MMM', 'UTX', 'PG', 'PFE', 'VZ', 'MSFT', 'KO','MRK', 'INTC', 'TRV', 'HD', 'GE', 'BA', 'AXP', 'GS', 'NKE', 'DIS', 'AAPL', 'UNH', 'V', 'CSCO', 'IBM', 'DD', 'XOM', 'JPM', 'CVX', 'CAT', 'MCD']
stock_url = ['Wal-Mart+Stores+stock', 'johnson+%26+johnson+stock', '3M+stock', 'United+Technologies+stock', 'Procter+%26+Gamble+stock', 'Pfizer+stock', 'Verizon+Communications+stock', 'Microsoft+Corporation+stock', 'Coca-Cola+stock', 'Merck+stock', 'Intel+stock', 'Travelers+Companies+stock', 'Home+Depot+stock', 'General+Electric+stock', 'Boeing+stock', 'American+Express+stock', 'Goldman+Sachs+stock', 'Nike+stock', 'Walt+Disney+stock', 'Apple+stock', 'UnitedHealth+Group+stock', 'Visa+stock', 'Cisco+stock', 'International+Business+Machines+stock', 'E.I.+du+Pont+de+Nemours+stock', 'Exxon+Mobil+stock', 'JP+Morgan+Chase+stock', 'Chevron+stock', 'Caterpillar+stock', "McDonald's+stock"]
stock_names = ['Wal-Mart','johnson','3M','United Technologies','Procter & Gamble','Pfizer', 'Verizon Communications', 'Microsoft', 'Coca-Cola', 'Merck', 'Intel', 'Travelers Companies', 'Home Depot', 'General Electric', 'Boeing', 'American Express', 'Goldman Sachs', 'Nike', 'Walt Disney', 'Apple', 'UnitedHealth', 'Visa', 'Cisco', 'International Business Machines', 'du Pont de Nemours', 'Exxon Mobil', 'JP Morgan Chase', 'Chevron', 'Caterpillar', 'McDonald']
code_url = dict(zip(slist, stock_url))
url_name = dict(zip(stock_url, stock_names))
i = 0
for stock in stock_url:
    for j in lst:
        google_link = 'https://www.google.co.in/search?q='+str(stock)+'&num=100&hl=en&gl=us&authuser=0&tbm=nws&ei=0krUWOD4H4rvvASI147AAg&start='+str(j)+'&sa=N&biw=1366&bih=635&dpr=1'
        page = requests.get(google_link) #url of reuters archive for 16.3.2017
        soup = BeautifulSoup(page.content,'html.parser')
        #print(soup.prettify())
        for item in soup.find_all(class_ = "g"):
            for link in item.find_all(class_ ="r"):
                title.append(link.get_text())
                for sublink in link.find_all('a'):
                    sstr = str(sublink.get('href'))
                    if(re.match(r'^\/url\?q=',sstr) != None):
                        b = re.search( r'^\/url\?q=(.*)', sstr.split('&')[0], re.I).group(1)
                        url.append(b)
                        names.append(url_name[stock])
                        print(b)
        for item in soup.find_all(class_ = "g"):
            for dat in item.find_all(class_="slp"):
                for source in dat.find_all(class_="f"):
                    newspapers.append(source.get_text().split('-')[0])
                    dates.append(source.get_text().split('-')[1])
                    i = i+1

#url = list(set(url))
print(len(url))
print(len(newspapers))
print(len(dates))
print(len(names))
print(len(title))

df = pd.DataFrame(np.nan, index=np.arange(0,len(url),1), columns=['url','Date','Newspaper','Title','Text','Stock.Name'])
df.iloc[:,0] = url
df.iloc[:,1] = dates
df.iloc[:,2] = newspapers
#df.iloc[:,3] = title
df.iloc[:,5] = names
pd.DataFrame.to_csv(df,'urls.csv',index=False, sep=',')
print('Done 1')

df = pd.read_csv('urls_truncated.csv',sep=',')
url = df.iloc[:,0]

print('Done Here')
def extractor(lst):
    i = 0
    for site in lst:
        try:
            print(site,i,'title')
            article = Article(site , language = 'en')
            article.download()
            article.parse()
            article.nlp()
            #df.iloc[i,3] = article.text
            df.iloc[i,3] = article.title
        except:
            print(site, "No title")
            pass
        try:
            print(site,i,'body')
            article = Article(site , language = 'en')
            article.download()
            article.parse()
            article.nlp()
            df.iloc[i,4] = article.text
        except:
            print(site, "No Body")
            pass
        i += 1
    return(site)

extractor(url)
pd.DataFrame.to_csv(df,'google_news_3000.csv',index=False, sep=',')