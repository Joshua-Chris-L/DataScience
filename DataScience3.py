#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df_tesla = pd.read_csv("TESLA.csv")

print(df_tesla)


# In[2]:


df_tesla.shape


# In[3]:


df_tesla.MONTH


# In[4]:


df_tesla.describe()


# In[5]:


df_unemployment = pd.read_csv("unemployment.csv")


# In[6]:


df_unemployment


# In[7]:


df_unemployment.describe() 


# In[8]:


import pandas as pd

df_btc = pd.read_csv("BitcoinSearchTrend.csv")

print(df_btc)


# In[9]:


import pandas as pd

df_btc_price = pd.read_csv("DbitconPrice.csv")

print(df_btc)


# In[10]:


df_tesla


# In[11]:


df_tesla['MONTH'] = pd.to_datetime(df_tesla['MONTH'],format='%Y-%m-%d')
df_tesla['year'] = pd.DatetimeIndex(df_tesla['MONTH']).year
df_tesla['year']


# In[12]:


tesla_web_search = df_tesla.TSLA_WEB_SEARCH
tesla_web_search


# In[13]:


import matplotlib.pyplot as plt
tesla_stock_price = df_tesla.TSLA_USD_CLOSE
tesla_stock_price


# In[14]:


import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import matplotlib.ticker as ticker

plt.figure(figsize=(14, 8))
plt.title('Tesla web Search vs Price', fontsize=18)

plt.xticks(fontsize=14, rotation=45)


ax1 = plt.gca()
ax2 = ax1.twinx()


#start, end = ax.get_xlim()

ax1.plot(df_tesla.MONTH, tesla_stock_price, color='r')
ax2.plot(df_tesla.MONTH, tesla_web_search, color='b')

# Set minimum and maximum values on the axis
ax1.set_ylim([0, 600])

#start, end = ax1.get_xlim()

#ax1.xaxis.set_ticks(np.arange(0, 600, 2))
# Create locators on the time axis
#years = mdates.YearLocator()
#months = mdates.MonthLocator()
#years_fmt = mdates.DateFormatter('%Y')


ax1.set_xlabel('year')
ax1.set_ylabel('TSLA stock price', color='red')
ax2.set_ylabel('TSLA web search', color='blue')


# In[15]:


df_app = pd.read_csv("apps.csv")

df_app


# In[16]:


df_app.sample(5)


# In[17]:


df_app.drop(["Last_Updated", "Android_Ver"], axis=1, inplace=True)

df_app


# In[18]:


df_app.isna()


# In[19]:


df_app_cleann = df_app.dropna()

df_app_cleann


# In[20]:


df_app_clean = df_app_cleann[df_app_cleann.duplicated()]

df_app_clean


# In[21]:


df_app_clean[df_app_clean.App == 'Instagram']


# In[22]:


df_app_clean.Rating.max()


# In[23]:


#use sort values when sorting out numbers from highest to lowest out of a given data

df_app_clean.sort_values('Rating', ascending=False).head()


# In[24]:


df_app_clean.sort_values('Size_MBs', ascending=False).head()


# In[25]:


df_app_clean.sort_values('Reviews', ascending=False).head()


# In[26]:


df_app_clean.sort_values('Price', ascending=False).head()


# In[27]:


#year = df_app_clean.groupby('Genres').count()


# In[28]:


ratings = df_app_cleann.Content_Rating.value_counts()

ratings


# In[29]:


# Using plotly for plotting instead on matplotlib
import plotly.express as px 

fig = px.pie(labels=ratings.index, values=ratings.values, title="Content Rating", names=ratings.index)
fig.update_traces(textposition='outside', textinfo='percent+label')

fig.show()


# In[30]:


# Using plotly for plotting instead on matplotlib
# Donuought shape using plotly

import plotly.express as px

fig = px.pie(labels=ratings.index, values=ratings.values, title="Content Rating", names=ratings.index, hole=0.8)
fig.update_traces(textposition='outside', textinfo='percent+label')

fig.show()


# In[31]:


df_app_clean.Installs.describe()


# In[32]:


df_app_clean.info()


# In[33]:


df_app_cleann[['App', 'Installs']].groupby('Installs').count()


# In[34]:


# remove the comma symbol from the sentence
df_app_cleann.Installs = df_app_cleann.Installs.astype(str).str.replace(',' , "")

# Replace the comma with space for installs column
df_app_cleann.Installs = pd.to_numeric(df_app_cleann.Installs)


# Display Values
df_app_cleann[['App', 'Installs']].groupby('Installs').count()


# In[35]:


df_app_cleann


# In[36]:


df_app_cleann.Price.describe()


# In[37]:


df_app_cleann.Price = df_app_cleann.Price.astype(str).str.replace('$', "")
df_app_cleann.Price = pd.to_numeric(df_app_cleann.Price)

df_app_cleann.sort_values('Price', ascending=False).head(20)


# In[38]:


df_app.cleann = df_app_cleann[df_app_cleann['Price'] < 250]

df_app_cleann.sort_values('Price', ascending=False).head(20)


# In[39]:


df_app_cleann['Revenue_Estimate'] = df_app_cleann.Installs.mul(df_app_cleann.Price)

df_app_cleann.sort_values('Revenue_Estimate', ascending=False)[:10]


# In[40]:


df_app_cleann.Category.nunique()


# In[41]:


top10_Category = df_app_cleann.Category.value_counts()[:10]

top10_Category


# In[42]:


bar = px.bar(x=top10_Category.index, y=top10_Category.values)
bar.show()


# In[43]:


category_installs = df_app_cleann.groupby('Category').agg({'Installs': pd.Series.sum})

category_installs
#category_installs.sort_values('Installs', ascending=True, inplace=True)


# In[44]:


h_bar = px.bar(x=category_installs.Installs, y=category_installs.index, orientation='h')

h_bar.show()


# In[45]:


cat_number = df_app_cleann.groupby('Category').agg({'App': pd.Series.count})
cat_number


# In[46]:


cat_merged_df = pd.merge(cat_number, category_installs, on='Category')

cat_merged_df.sort_values('Installs', ascending=False)


# In[47]:


scatter = px.scatter(cat_merged_df, x='App', y='Installs', title='Category Concentration', 
                     size='App', hover_name=cat_merged_df.index, color='Installs')


scatter.update_layout(xaxis_title='Number of Apps (Lower=More Concentration)',
                     yaxis_title = "Installs",
                      yaxis=dict(type='log')
                     )

scatter.show()


# In[48]:


df_app_cleann.Genres.describe()


# In[57]:


df_app_cleann


# In[59]:


Genres_df = df_app_cleann.groupby('Genres').agg({'App': pd.Series.count})
Genres_df


# In[73]:


Genres_df.App


# In[77]:


df_app_cleann.Type.value_counts()


# In[50]:


df_app_cleann.Genres.value_counts().sort_values(ascending=True)[:5]


# In[51]:


#Split the nested string and stack
stack = df_app_cleann.Genres.str.split(',', expand=True).stack()
stack.shape


# In[68]:


Genres_df.values[:15]


# In[75]:


barr = px.bar(x=Genres_df.index[:15], y=Genres_df.values[:15])

barr.show()


# In[64]:


bar = px.scatter(x=stack.index[:15], y=stack.values[:15], 
                 title='Top Genres', hover_name=stack.index[:15], color=stack.values[:15],
                    color_continuous_scale='Agsunset')


bar.update_layout(xaxis_title='Genre',
                     yaxis_title = "Number of Apps",
                     coloraxis_showscale=False)

bar.show()


# In[76]:


df_app_cleann.Type.value_counts()


# In[90]:


df_free_vs_paid = df_app_cleann.groupby(["Category", "Type"], as_index=False).agg({'App': pd.Series.count })

df_free_vs_paid.head(20)


# In[92]:


g_bar = px.bar(df_free_vs_paid,
               x='Category', y='App',
               title='Free vs Paid Apps by Category',
               color='Type',
               barmode='group')

g_bar.update_layout(xaxis_title='Category',
                    yaxis_title='Number of Apps',
                    xaxis={'categoryorder':'total descending'},
                    yaxis=dict(type='log'))

g_bar.show()


# In[84]:


df_free_vs_paid = df_app_cleann.groupby(["Category"], as_index=False).agg({'App': pd.Series.count })

df_free_vs_paid.head(20)


# In[93]:


box = px.box(df_app_cleann,
             y='Installs',
             x='Type',
             color='Type',
             notched=True,
             points='all',
             title='How many dowloads are paid apps giving up ?'
)

box.update_layout(yaxis=dict(type='log'))

box.show()


# In[96]:


df_paid_app = df_app_cleann[df_app_cleann['Type'] == 'Paid']

df_paid_app


# In[99]:


box = px.box(df_paid_app, 
            x='Category',
            y='Revenue_Estimate',
            title='How much can paid apps earn?'
            )
box.update_layout(xaxis_title = 'Category',
                  yaxis_title = 'Paid App Ballpark Revenue',
                  xaxis={'categoryorder': 'min ascending'},
                  yaxis=dict(type='log'))


box.show()


# In[100]:


df_paid_app.Price.median()


# In[101]:


box_price = px.box(df_paid_app,
                x='Category',
                y='Price',
                title='Price per Category')

box.update_layout(xaxis_title = 'Category',
                  yaxis_title = 'Paid App Price',
                  xaxis={'categoryorder': 'max descending'},
                  yaxis=dict(type='log'))

box.show()


# In[ ]:




