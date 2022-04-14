#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
from ast import literal_eval
import re


# In[38]:


headline=pd.read_csv('./data/headline/Classified_headline.csv')


# In[39]:


headline


# In[40]:


def datechange(x):
    if len(x) == 19:
        d = datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
    else:
        d = datetime.strptime(x,'%Y-%m-%d %H:%M')
    d2 = datetime(year = d.year,month=d.month,day=d.day,hour=15,minute = 30)
    w = d2.weekday()
    if w >= 4:
        if w == 4:
            if d > d2:
                day = d.date()
            else:
                day = d.date() - dt.timedelta(days=1)
        else:
            day = d.date() - dt.timedelta(days=w-4)
    else:
        if d > d2:
            day = d.date()
        else:
            day = d.date() - dt.timedelta(days=1)
    return day


# In[45]:


def agg(x):
    a = x.pivot_table(index = 'Date', values='vector', aggfunc=['count','sum'])
    b = pd.DataFrame()
    b['Date'] = list(a.index)
    b['vector'] = (a['sum']/a['count']).values
    return b


# In[ ]:


#code dealing str vector
#r = headline.vector.apply(lambda x: re.sub(' +','',x[:2])+re.sub(' +',',',x)[2:])
#r2 = r.apply(literal_eval)
#r3 = r2.apply(np.array)
#headline.vector = r3

