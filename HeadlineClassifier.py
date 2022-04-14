#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import pyemd

from konlpy.tag import Kkma
from konlpy.tag import Okt
from tqdm import tqdm
from gensim.models import Word2Vec

tqdm.pandas()


# In[18]:


def doc2vec(doc,model,vocab):
        doc_vec = np.zeros(100)
        for i in doc:
            if i not in vocab:
                continue
            doc_vec+=model.wv.get_vector(i)
        return doc_vec
    
def mapping_industry(x, ind_vec, model, vocab):
        head_vec = doc2vec(x,model,vocab)
        if any(pd.Series(['기온','날씨','더위','폭염','영하']).isin(x)):
            similarity = np.array([0,0,0])
            return similarity
        similarity = model.wv.cosine_similarities(head_vec,ind_vec)
        return similarity
    
class HeadlineClassifier:
    
    def __init__(self,model = Word2Vec.load('./model/Headline.model'),
                 df = pd.read_csv('./data/headline/New_headline.csv',index_col=0)):
        self.model = model
        self.vocab = model.wv.index2word
        self.df = df
        self.okt= Okt()
        
        print('tokenizing title')
        self.df['token'] = self.df.title.progress_apply(self.okt.nouns)

    def classify(self):
        x=self.df.copy()

        semi = ['반도체','하이닉스','램','메모리','인텔','파운드리','EUV','TSMC','플래시']
        bio = ['헬스케어','바이오','바이오벤처','삼성바이오','셀트리온','의약','백신','신약']
        tel = ['유플러스','통신사','케이티','엘지','㎓','텔레콤','SKT','KT','주파수']
        
        print('make industry vectors')
        self.ind_vec = np.array([doc2vec(semi,self.model,self.vocab),
                                doc2vec(bio,self.model,self.vocab),
                                doc2vec(tel,self.model,self.vocab)])


        x['industry'] = x.token.progress_apply(mapping_industry,args=[self.ind_vec,self.model,self.vocab])
        x2 = x.copy()
        x2 = x2[x2.industry.apply(lambda x: ~np.isnan(x)[0])]
        x2['ind_index']=x2.industry.progress_apply(lambda z: list(z).index(max(z)))
        x2.reset_index(inplace=True,drop=True)

        threshold = 0.005
        for i in range(len(x2)):
            v = np.var(x2.industry[i])
            if v < threshold:
                x2.ind_index[i] = 3

        threshold = 0.55
        for i in range(len(x2)):
            m = max(x2.industry[i])
            if m < threshold:
                x2.ind_index[i] = 3

        x2['산업']=x2.ind_index.replace({0:'반도체',1:'바이오',2:'통신',3:'None'})
        x2['vector']=x2.token.progress_apply(doc2vec,args=[self.model,self.vocab])

        return x2        


# In[ ]:




