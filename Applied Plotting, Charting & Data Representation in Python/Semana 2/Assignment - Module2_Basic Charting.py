#SOLUCIÓN ASSIGNMENT 2!!!

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

file=pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
data=file.sort_values('Date')
data=data[data["Date"]< '2015-01-01']
data['Date'] = data['Date'].apply(lambda x: (re.split("[\d]{4}[-]",x)[-1])) #CLEANING
# data=data.set_index('Date')
# data=data.drop(['02-29'], axis=0)
data= data[data['Date'] != '02-29']

data['Data_Value']=data['Data_Value']/10

TMIN=data.groupby('Date').agg({'Data_Value':np.min})
TMAX=data.groupby('Date').agg({'Data_Value':np.max})

plt.plot(TMAX.values, color='#F28100', label='Record High')
plt.plot(TMIN.values, color='#0023B2', label='Record Low')

plt.gca().fill_between(range(len(TMAX)), 
                       TMAX.values.reshape(len(TMIN.values)), 
                       TMIN.values.reshape(len(TMIN.values)),
                       facecolor='#99B5FF', 
                       alpha=0.25)

plt.xlabel('Day')
plt.ylabel('Temperature (°C)')
plt.title('Temperature records of a decade (2005-2014) exceeded in 2015')
plt.gca().axis([0,365,-32,42])

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# DATOS 2015

data2015=file.sort_values('Date')
data2015=data2015[data2015["Date"] > '2014-12-31']
data2015['Date'] = data2015['Date'].apply(lambda x: (re.split("[\d]{4}[-]",x)[-1])) #CLEANING

data2015['Data_Value']=data2015['Data_Value']/10
TMIN2015=data2015.groupby('Date').agg({'Data_Value':np.min})
TMAX2015=data2015.groupby('Date').agg({'Data_Value':np.max})

all_max = pd.merge(TMAX.reset_index(), TMAX2015.reset_index(), how="inner", on=['Date'])
all_max
all_min = pd.merge(TMIN.reset_index(), TMIN2015.reset_index(), how="inner", on=['Date'])
all_min

record_max = all_max[all_max['Data_Value_y'] > all_max['Data_Value_x']]
record_min = all_min[all_min['Data_Value_y'] < all_min['Data_Value_x']]
record_max

plt.scatter(record_max.index.tolist(), record_max['Data_Value_y'].values, color='#D21100', s=10, label='Broken High T 2015')
plt.scatter(record_min.index.tolist(), record_min['Data_Value_y'].values, color='#00073F', s=10, label='Broken Low T 2015')

plt.legend(loc='best', fontsize=8)
