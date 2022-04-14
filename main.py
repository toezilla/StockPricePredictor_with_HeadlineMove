#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pickle
import datetime as dt
from datetime import datetime

import tensorflow as tf
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

import CrawlingHeadline
import HeadlineClassifier
from HeadlineMove import datechange, agg

tqdm.pandas()

# In[ ]:


if __name__=='__main__':
    
    df = CrawlingHeadline.crawiling_headline()
    with open('./data/vector/headline_vector.pickle','rb') as fr:
        vector = pickle.load(fr)
    
    now = datetime.now()
    if now < datetime(year=now.year,month=now.month,day=now.day,hour=15,minute=30):
        now = now - dt.timedelta(days=1)
    today = now.strftime('%Y-%m-%d')

    print('Updating headline data and Vector')
    if len(df) > 0:
        import re
        from ast import literal_eval
        print('Classify new headline')
        
        clf = HeadlineClassifier.HeadlineClassifier(df = df)
        df_clf = clf.classify()
        df_clf.to_csv('./data/headline/New_headline_Classified.csv',index=False)
        print('Save classifed headline')
        
        headline = pd.read_csv('./data/headline/Classified_headline.csv')

        print('Processing headline data')
        headline.vector = headline.vector.progress_apply(lambda x: re.sub(' +','',x[:2])+re.sub(' +',',',x)[2:])
        headline.vector = headline.vector.progress_apply(literal_eval)
        headline.vector = headline.vector.progress_apply(np.array)
        
        headline = pd.concat([df_clf,headline])
        headline.to_csv('./data/headline/Classified_headline.csv',index=False)
        
        print('Make new vectors of new headlines')
        headline['date'] = headline.date.progress_apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if type(x)!=str else x)
        headline['Date'] = headline.date.apply(datechange)
        industry = {i:headline[headline.산업 == i][['Date','산업','title','vector']] for i in ['반도체','바이오','통신']}
        
        bio = agg(industry['바이오'])
        semi = agg(industry['반도체'])
        tel = agg(industry['통신'])
        
        new_vector = {}
        for j,k in [(semi,'반도체'),(bio,'바이오'),(tel,'통신')]:
            s = pd.DataFrame(j.vector.values[0]).T
            for i in j.vector.values[1:]:
                b = pd.DataFrame(i).T
                s = pd.concat([s,b])
            s['Date'] = list(j.Date)
            s.reset_index(inplace=True,drop=True)
            new_vector[k] = s
            
        vector = new_vector
        print('Save new vector file')
        with open('./data/vector/headline_vector.pickle','wb') as fw:
            pickle.dump(vector, fw)        
    print('Headline data is ready!')
    
    model=tf.keras.models.load_model('./model/stock_model_raw_news.h5')
    
    while True:
        stock_key = ''
        stock_index = []
        ind = ['반도체','바이오','통신']
        stocks = pd.DataFrame(columns = ['Open','High','Low','Close','Volume'])
        stock_key = input('예측을 수행할 주식의 번호를 입력해주세요. (취소:N/n)')
        while stock_key != 'N' and stock_key!='n' :
            
            
            i = input('회사의 산업 분야를 선택해주세요.\n1: 반도체\n2: 바이오\n3: 통신\n')
            
            while i not in ['1','2','3']:
                print('1,2,3번 중 선택해주세요.')
                i = input('회사의 산업 분야를 선택해주세요.\n1: 반도체\n2: 바이오\n3: 통신\n')
            
            idstry = ind[int(i)-1]
            
            stock = fdr.DataReader(stock_key,'2018-01-01',  today)
            stock_index.append(stock_key)
            
            stock.reset_index(inplace=True)
            stock['Date'] = stock.Date.apply(lambda x:x.date())
            
            col = list(stock.columns)
            col.pop()
            col.pop(0)
            
            scaler = MinMaxScaler()
            scaler.fit(stock.loc[:,col])
            
            with open('./scaler/{}_scaler.pickle'.format(stock_key),'wb') as fw:
                pickle.dump(scaler,fw)
            
            stock = stock.iloc[-21:,:].reset_index(drop=True)
            
            yesterday_x = stock.loc[:19,['Date']+col]
            yesterday_x.loc[:,col] = scaler.transform(yesterday_x.loc[:,col])
            
            yesterday_x = pd.merge(yesterday_x,vector[idstry],on='Date',how='left').fillna(0)
            del yesterday_x['Date']
            
            yesterday_y = stock.loc[20,col].values
            with tf.device('CPU:0'):
                yesterday_pred = scaler.inverse_transform(model.predict(yesterday_x.values.reshape(1,20,105)))
            err = yesterday_y-yesterday_pred
            
            X = stock.loc[1:20,['Date']+col]
            X.loc[:,col] = scaler.transform(X.loc[:,col])
            X = pd.merge(X,vector[idstry],on='Date',how='left').fillna(0)
            del X['Date']
            
            with tf.device('CPU:0'):
                pred = scaler.inverse_transform(model.predict(X.values.reshape(1,20,105)))
            pred = pred + err
            
            cnt=0
            temp = yesterday_y[-2]
            while temp%10 == 0:
                temp/=10
                cnt += 1
            
            pred = (pred*(0.1**cnt)).astype('int')*(10**cnt)
            pred = pd.DataFrame(pred,index=[stock_key],columns=col)
            
            
            print(pred[col[:-1]])
            stocks = pd.concat([stocks,pred])
            stock_key = input('예측을 수행할 주식의 번호를 입력해주세요. (취소:N/n)')
        
        del stocks['Volume']
        print(stocks)
        end = input('end?[y/n]')
        if end == 'y' or end == 'Y':
            break
            


# In[ ]:




