#%%
import pandas as pd
import numpy as np
import os 
import matplotlib.pyplot as plt
import plotly.offline as pyo
pyo.init_notebook_mode()
#import plotly.graph_objects as go
#import plotly.express as px
import seaborn as sns


#%% data acquisition 
fn = "Question 2. Database.xlsx"
df = pd.read_excel(fn,header=0)
df = df.sort_values(['LifeID','UW Date']).drop_duplicates(['LifeID','UW Date'])
df

# %% Data cleaning / augmentation 
import datetime as dt
# df['Age@uw']=(df['UW Date']-df['DOB']) #dt.timedelta(df['UW Date'], df['DOB'])
# df['Age@uw']=df['Age@uw'].apply(lambda x: x.days/365) #apply(days/365)
# df 
#%% compare first UW to last 

dff = df.loc[df.groupby('LifeID')['UW Date'].rank(method='dense',ascending=True)==1,:] 
dfl = df.loc[df.groupby('LifeID')['UW Date'].rank(method='dense',ascending=False)==1,:]
#len(list(dfl.LifeID)), len(list(dff.LifeID))
df1 = pd.merge(dff,dfl,on='LifeID')
df1.drop(columns=['DOB_y','DOD_y','Gender_y'],inplace=True)
df1 = df1[df1['UW Date_y']>df1['UW Date_x']]
df1['MRchange']=df1['MR_y']-df1['MR_x']
df1['periodUW']=(df1['UW Date_y']-df1['UW Date_x']).apply(lambda x: x.days/365)
df1['Age_x']=(df1['UW Date_x']-df1['DOB_x']).apply(lambda x: x.days/365)
df1['Age_y']=(df1['UW Date_y']-df1['DOB_x']).apply(lambda x: x.days/365)

#df[df['lastUW']==True]
df1.head(50)


#%% influence of age 
""" rating according to age at time of UW """
df1.plot.scatter(x='Age_x', y='MR_x',c='darkblue',alpha=.3)
df1.plot.scatter(x='Age_y', y='MR_y',c='darkred',alpha=.3)

""" rem 1: there are some "default MR" at both initial and final UW at 1500% and 2000%"""
df1[df1['MR_x']==15]['Impair_x'].value_counts()
""" the vast majority of people with HIV/AIDS is rated 1500% by default with only slight evolution at final UW """
df1[df1['MR_y']==15]['Impair_x'].value_counts()
""" One condition is not a disease; 'Elder'appears rating as 2000%"""
df1[df1['MR_y']==20]['Impair_x'].value_counts()

""" rem 2: the population has aged at the final UW, and the ratings of olders insured have increased """


#%%

""" Rating evolution (MR_x to MR_y) over the database  """
# plot terminal MR vs initial 
df1[['MR_x','MR_y']].plot.scatter(x='MR_x', y='MR_y',c='darkblue')

"""graph initial MR per condition """
df1['Impair_x'].fillna(value='unkown',inplace=True)
sorter = list(df1.groupby('Impair_x')[['MR_x']].mean().sort_values('MR_x',ascending=False).index)
sorterIndex = dict(zip(sorter, range(len(sorter))))
df1['Impairorder']=df1['Impair_x'].map(sorterIndex)
df1.sort_values('Impairorder').plot.scatter(x='Impair_x',y='MR_x',c='blue',rot=90, alpha=.3,figsize=(20,7))

#df1[df1['Impair_x'].str.startswith('CA ')].plot.scatter(x='Impair_x',y='MR_x',c='blue',rot=90, alpha=.3)

""" List of diseases with best Rating improvement """
pd.options.display.float_format = '{:.2%}'.format
pd.concat([df1.groupby('Impair_x')[['MR_x']].count().rename(columns={'MR_x':'nb'}),\
    df1.groupby('Impair_x')[['MR_x','MR_y','MRchange']].mean().rename(columns={'MR_x':'MR init','MR_y':'MR final'})],axis=1)\
    .sort_values('MRchange',ascending=True).head(30)

""" evolution rating for 1 condition wrt time of UW"""
cname = 'Sarcoma – soft tissue' #'CA Pancreas' #'Scleroderma'
llife=list(df1.loc[df1['Impair_x']==cname,'LifeID'])
df2=df[df['LifeID'].isin(llife)].copy()
df2['initUW']=df2['LifeID'].map(dict(zip(df1['LifeID'],df1['UW Date_x'])))
df2['UWperiod']=(df2['UW Date']-df2['initUW']).apply(lambda x: x.days/365)
df2.plot.scatter(x='UWperiod',y='MR',c='red',style="b",title=f'evolution of ratings for all insured with {cname}')



#%%  Analysis for specific disease 
