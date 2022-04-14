#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import requests
import time
import re
from tqdm import tqdm
import datetime as dt
from datetime import datetime

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib import parse

tqdm.pandas()


# In[27]:


def crawiling_headline():
    path = './data/headline/'
    dong = pd.read_csv(path+'Updated_headline.csv',index_col=0)
    
    print('str to datetime')
    dong['date'] = dong['date'].progress_apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    last=dong['date'][0]
    print('Last day: {}'.format(last))
    
    page=1
    title = []
    date = []
    
    print('Now crawling Headline data',end = '')
    while True:
        url = 'https://www.donga.com/news/It/List?p={}&prod=news&ymd=&m='.format(page)
        html = urlopen(url)
        soup = bs(html,'html.parser')
        a = soup.find_all('div',{'class':'articleList'})
        for i in a:
            title .append(i.find('span',{'class':'tit'}).text)
            d=i.find('span',{'class':'date'}).text
            d=datetime.strptime(d,'%Y-%m-%d %H:%M')
            date.append(d)
        if  d<= last:
            break
        page+=20
        print('.',end='')
    print('\nEnd Crawling Headline')
    
    df = pd.DataFrame({'date':date,'title':title})
    df = df[df['date']>last]
    df.reset_index(inplace=True, drop=True)
    
    print('save new headline to '+path)
    df.to_csv(path+'/New_headline.csv')
    
    dong = pd.concat([df,dong])
    dong.reset_index(inplace=True,drop=True)
    
    print('save updated headlint to '+path)
    dong.to_csv(path+'Updated_headline.csv')
    
    return df

