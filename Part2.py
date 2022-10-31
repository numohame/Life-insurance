#%% Load library
import os
os.chdir(r'C:\Users\sharu\Documents\CV\UpWork\Adam Ramin\Life Insurance')
import pandas as pd
import matplotlib.pyplot as plt

# Default plot settings
plt.rc(group = "figure", figsize = (16, 9))
plt.rc(group = "font", size = 14)

#%% Import data
df = pd.read_excel('Question 2. Database.xlsx')
df = df.sort_values(['LifeID', 'UW Date']).drop_duplicates(['LifeID', 'UW Date'])
df

#%% Change of MR from first UW to last
df_first = df.loc[df.groupby('LifeID')['UW Date'].rank(method = 'dense', ascending = True) == 1, :] 
df_last = df.loc[df.groupby('LifeID')['UW Date'].rank(method = 'dense', ascending = False) == 1, :]
df1 = pd.merge(df_first, df_last, on = 'LifeID')
df1.drop(columns = ['DOB_y', 'DOD_y', 'Gender_y'], inplace = True)
df1 = df1[df1['UW Date_y'] > df1['UW Date_x']]
df1['MR_change'] = df1['MR_y'] - df1['MR_x']
df1['periodUW'] = (df1['UW Date_y'] - df1['UW Date_x']).apply(lambda x: x.days / 365)
df1['Age_x'] = (df1['UW Date_x'] - df1['DOB_x']).apply(lambda x: x.days / 365)
df1['Age_y'] = (df1['UW Date_y'] - df1['DOB_x']).apply(lambda x: x.days / 365)
df1.head(50)

#%% Change in Average Mortality Rating by Gender
pd.options.display.float_format = '{:.2%}'.format
df_temp = pd.concat([df1.groupby('Gender_x')[['MR_x']].count().rename(columns={'MR_x':'#Cases'}),\
                     df1.groupby('Gender_x')\
                         [['MR_x','MR_y','MR_change']].mean().rename(columns=\
                                                                    {'MR_x':'MR_initial',
                                                                     'MR_y':'MR_final'})],
                    axis = 1)\
    .sort_values('MR_change',ascending=True).head(30)
df_temp.index.name = 'Gender'
df_temp

#%% Change in Average Mortality Rating by Type of Health Impairment
df_temp = pd.concat([df1.groupby('Impair_x')[['MR_x']].count().rename(columns={'MR_x':'#Cases'}),\
                     df1.groupby('Impair_x')\
                         [['MR_x','MR_y','MR_change']].mean().rename(columns=\
                                                                    {'MR_x':'MR_initial',
                                                                     'MR_y':'MR_final'})],
                    axis = 1)\
    .sort_values('MR_change',ascending=True).head(30)
df_temp.index.name = 'Impair'
df_temp

#%% Average Mortality Rating by Time Till Death
# Add a new columne 'TimeTillDeath'
df['TimeTillDeath'] = (df['DOD'] - df['UW Date']).astype('timedelta64[Y]')
df['TimeTillDeath'].value_counts()
df = df[df['TimeTillDeath']>=0]
df_MR_mean_by_age = df.groupby('TimeTillDeath').mean()['MR'] * 100
df_MR_mean_by_age.plot()
plt.ylabel('MR (%)')
plt.title('Average Mortality Rating by Time Till Death')

