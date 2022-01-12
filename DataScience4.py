#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np

import matplotlib.pyplot as plt
from scipy import misc # contain an image of a racoon
from PIL import Image # Reading images from files

my_array = np.array([1.1, 9.2, 8.1, 4.7])

my_array.shape


# In[18]:


array_2D = np.array([[1.1, 9.2, 8.1, 4.7], [1, 9.5, 8, 4.9]])


# In[19]:


noise = np.random.random((128, 128, 3))
print(noise.shape)
plt.imshow(noise)


# In[20]:


noise = np.random.random((20, 41, 3))
print(noise.shape)
plt.imshow(noise)


# In[21]:


img = misc.face()

plt.imshow(img)


# In[22]:


type(img)


# In[23]:


sRGB_array = img/255


# In[24]:


grey_vals = np.array([0.2126, 0.7152, 0.0722])

img_gray = sRGB_array@ grey_vals

plt.imshow(img_gray, cmap='gray')


# In[25]:


plt.imshow(img_gray)


# In[42]:


import pandas as pd
df = pd.read_csv("cost_revenue_dirty.csv")
df


# In[43]:


#Check for null values

df.isnull().values.any()


# In[44]:


# duplicated rows
df.duplicated().values.any()


# In[46]:


# duplicated values

duplicated_rows = df[df.duplicated()]

len(duplicated_rows)


# In[48]:


df.info()


# In[55]:


chars_to_remove = [',', '$']
columns_to_clean = ['USD_Production_Budget',
                   'USD_Worldwide_Gross',
                    'USD_Domestic_Gross']

for col in columns_to_clean:
    for char in chars_to_remove:
        df[col] = df[col].astype(str).str.replace(char, "")
    df[col] = pd.to_numeric(df[col])


# In[56]:


df


# In[57]:


df.Release_Date = pd.to_datetime(df.Release_Date)


# In[58]:


df


# In[59]:


df.describe()


# In[60]:


df[df.USD_Production_Budget == 1100.00]


# In[62]:


df[df.USD_Production_Budget == 425000000]


# In[65]:


zero_worldwide = df[df.USD_Worldwide_Gross == 0]

zero_worldw
ide


# In[66]:


len(zero_worldwide)


# In[69]:


international_releases = df.loc[(df.USD_Domestic_Gross == 0) & (df.USD_Worldwide_Gross != 0)]

international_releases


# In[73]:


# Use the query function to achieve the above

international_releases = df.query('USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0')

international_releases.tail()


# In[74]:


scrap_data = pd.Timestamp('2018-5-1')


# In[77]:


future_release = df[df.Release_Date >= scrap_data]

future_release


# In[79]:


df_clean = df.drop(future_release.index)

df_clean


# In[81]:


monney_losing = df_clean.loc[df_clean.USD_Production_Budget > df_clean.USD_Worldwide_Gross]

monney_losing


# In[85]:


international_releases = df_clean.query('USD_Production_Budget > USD_Worldwide_Gross')

international_releases


# In[89]:


import seaborn as sns

sns.scatterplot(data=df_clean,
                x='USD_Production_Budget',
                y='USD_Worldwide_Gross')


# In[94]:


plt.figure(figsize=(8,4), dpi=200)


import seaborn as sns

with sns.axes_style('darkgrid'):
    ax = sns.scatterplot(data=df_clean,
                    x='USD_Production_Budget',
                    y='USD_Worldwide_Gross',
                    hue ='USD_Worldwide_Gross', #color
                    size = 'USD_Worldwide_Gross')

    ax.set(ylim=(0, 3000000000),
           xlim = (0, 450000000),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions'
          )

    plt.show()


# In[97]:


dt_index = pd.DatetimeIndex(df_clean.Release_Date)

year = dt_index.year

year


# In[102]:


decades = year//10*10

# Create a new column with the data decades
df_clean['Decade'] = decades

df_clean.head(15)


# In[106]:



old_films = df_clean.query('Decade <= 1970')

old_films.head(20)


# In[108]:


new_films = df_clean.query('Decade > 1970')

new_films


# In[109]:


sns.regplot(data=old_films, 
           x='USD_Production_Budget',
           y= 'USD_Worldwide_Gross' )


# In[114]:


plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('whitegrid'):
    sns.regplot( data= old_films, 
    x = 'USD_Production_Budget',
    y = 'USD_Worldwide_Gross',
    scatter_kws = {'alpha': 0.4},
    line_kws = {'color': 'black'})
    
    


# In[130]:


plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('whitegrid'):
    ax = sns.regplot( data= old_films, 
        x = 'USD_Production_Budget',
        y = 'USD_Worldwide_Gross',
        color = '#2f4b7c',
        scatter_kws = {'alpha': 0.4},
        line_kws = {'color': '#ff7c43'})

ax.set(ylim=(0, 300000000),
      xlim=(0, 45000000),
      ylabel='Revenue in $ billion',
      xlabel = 'Budget in $100 millions')
    


# In[133]:


from sklearn.linear_model import LinearRegression

regression = LinearRegression()

X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])

Y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])

regression.fit(X,Y)


# In[ ]:




