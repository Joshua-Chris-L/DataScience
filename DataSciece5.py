#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd

df = pd.read_csv('nobel_prize_data.csv')

df.head(20)


# In[7]:


df


# In[9]:


df.info()


# In[10]:


df.isna().sum()


# In[19]:


df.head(3)


# In[21]:


col_subset = ['year', 'category', 'laureate_type', 'birth_date', 'full_name', 'organization_name']

df.loc[df.organization_name.isna()][col_subset]


# In[24]:


df.birth_date = pd.to_datetime(df.birth_date)

df.tail()


# In[25]:


seperated_values = df.prize_share.str.split('/', expand=True)

numerator = pd.to_numeric(seperated_values[0])
denominator=pd.to_numeric(seperated_values[1])
df['share_pct'] = numerator/denominator


# In[27]:


df.head()


# In[38]:


import plotly.express as px

biology = df.sex.value_counts()

fig = px.pie(labels=biology.index,
             values=biology.values,
             title='Percentage of Male vs Female winners',
             names=biology.index,
             hole=0.4) 

fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')

fig.show()


# In[39]:


biology


# In[41]:


df[df.sex == 'Female'].sort_values('year', ascending=True)[:3]


# In[49]:


is_winner = df.duplicated(subset=['full_name'], keep=False)

multiple_winners = df[is_winner]

multiple_winners #.full_name.nunique() 


# In[48]:


col_subset = ['year', 'category', 'laureate_type', 'full_name']

multiple_winners[col_subset]


# In[52]:


prize_per_category = df.category.value_counts()

v_bar = px.bar(
            x = prize_per_category.index,
            y = prize_per_category.values,
            color = prize_per_category.values, 
            color_continuous_scale='Aggrnyl',
            title='Number of prizes awarded per Category')

v_bar.update_layout(xaxis_title = 'Nobel Prize Category',
                    coloraxis_showscale = False,
                    yaxis_title = 'Number of Prizes')

v_bar.show()


# In[59]:


cat_men_women = df.groupby(['category', 'sex'], as_index = False).agg({'prize': pd.Series.count})


# In[61]:



cat_men_women #.sort_values('prize', ascending=False, inplace=True) 


# In[63]:


prize_per_category = df.category.value_counts()

v_bar = px.bar(
            x = cat_men_women.category,
            y = cat_men_women.prize,
            color = cat_men_women.sex, 
            color_continuous_scale='Aggrnyl',
            title='Number of prizes awarded per Category')

v_bar.update_layout(xaxis_title = 'Nobel Prize Category',
                    coloraxis_showscale = False,
                    yaxis_title = 'Number of Prizes')

v_bar.show()


# In[64]:


df


# In[71]:


prize_per_year = df.groupby('year').count().prize

moving_average = prize_per_year.rolling(window= 5).mean()

moving_average


# In[72]:


import matplotlib.pyplot as plt
plt.scatter(x=prize_per_year.index,
            y=prize_per_year.values,
            c='dodgerblue',
            alpha=0.7,
            s=100)

plt.plot(prize_per_year.index,
         moving_average.values,
         c='crimson',
         linewidth=3)

plt.show()


# In[ ]:


np.arrange(1900, 2021, step=5)


# In[76]:


import numpy as np

plt.figure(figsize=(16,8), dpi=200)

plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)

plt.yticks(fontsize=14)
plt.xticks(np.arange(1900, 2021, step=5),
         fontsize=14,
        rotation=45)

ax = plt.gca()
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           c='dodgerblue',
           alpha=0.7,
           s=100)

ax.plot(prize_per_year.index,
        moving_average.values,
        c='crimson',
        linewidth=3)


# In[77]:


df


# In[83]:


yearly_avg_share = df.groupby(by='year').agg({'share_pct': pd.Series.mean})

share_moving_average = yearly_avg_share.rolling(window=5).mean()

yearly_avg_share


# In[84]:


share_moving_average


# In[85]:


import numpy as np

plt.figure(figsize=(16,8), dpi=200)

plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)

plt.yticks(fontsize=14)
plt.xticks(np.arange(1900, 2021, step=5),
         fontsize=14,
        rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2020)

ax1.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           c='dodgerblue',
           alpha=0.7,
           s=100)

ax1.plot(prize_per_year.index,
        moving_average.values,
        c='crimson',
        linewidth=3)

ax2.plot(prize_per_year.index,
        share_moving_average.values,
        c='grey',
        linewidth=3)

plt.show()


# In[86]:


plt.figure(figsize=(16,8), dpi=200)

plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)

plt.yticks(fontsize=14)
plt.xticks(np.arange(1900, 2021, step=5),
         fontsize=14,
        rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2020)


ax2.invert_yaxis()

ax1.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           c='dodgerblue',
           alpha=0.7,
           s=100)

ax1.plot(prize_per_year.index,
        moving_average.values,
        c='crimson',
        linewidth=3)

ax2.plot(prize_per_year.index,
        share_moving_average.values,
        c='grey',
        linewidth=3)

plt.show()


# In[87]:


df


# In[97]:


top_countries = df.groupby(['birth_country_current'], as_index=False).agg({'prize': pd.Series.count})
top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]


# In[98]:


h_bar = px.bar(x=top20_countries.prize,
               y=top20_countries.birth_country_current,
               orientation='h',
               color=top20_countries.prize,
               color_continuous_scale = 'Viridis',
               title='Top 20 countries by number of prizes')

h_bar.update_layout(xaxis_title='Number of prizes',
                    yaxis_title='Country',
                    coloraxis_showscale=False)
h_bar.show()


# In[91]:


top_countries[:-20]


# In[100]:


df_countries = df.groupby(['birth_country_current', 'ISO'], as_index=False).agg({'prize':pd.Series.count})

df_countries.sort_values('prize', ascending=False)


# In[104]:


world_map = px.choropleth(df_countries,
                          locations='ISO',
                          color='prize',
                          hover_name = 'birth_country_current',
                          color_continuous_scale=px.colors.sequential.matter)

world_map.update_layout(coloraxis_showscale=True)

world_map.show()


# In[105]:


df


# In[172]:


cat_country = df.groupby(['birth_country_current', 'category'], as_index=False).agg({'prize': pd.Series.count})

cat_country.sort_values(by='prize', ascending=False, inplace=True)
cat_country


# In[173]:


top_countries = top_countries.sort_values(by='prize', ascending=False)


# In[174]:


merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')

#change column names
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize']

merged_df.sort_values(by='total_prize', inplace=True)


# In[175]:


top20_countries.head(3)


# In[176]:


merged_df


# In[177]:


cat_cntry_bar = px.bar(x=merged_df.cat_prize,
                      y=merged_df.birth_country_current,
                      color = merged_df.category,
                      orientation= 'h',
                      title='Top 20 countries by Number of prizes and Category')

cat_cntry_bar.update_layout(xaxis_title = 'Number of Prizes',
                            yaxis_title = 'Country')

cat_cntry_bar.show()


# In[178]:


prize_by_year = df.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]


# In[ ]:





# In[179]:


cummulative_prizes = prize_by_year.groupby(['birth_country_current', 'year']).sum().groupby(level=[0]).cumsum()

cummulative_prizes.reset_index(inplace=True)

cummulative_prizes


# In[180]:


l_chart = px.line(cummulative_prizes,
                  x='year',
                  y='prize',
                  color='birth_country_current',
                  hover_name='birth_country_current')

l_chart.update_layout(xaxis_title='year', 
                     yaxis_title='Number of Prizes')

l_chart.show()


# In[189]:


top20_orgs = df.organization_name.value_counts()[:20]

top20_orgs.sort_values(ascending=True, inplace=True)


# In[190]:


top20_orgs


# In[191]:


org_bar = px.bar( x = top20_orgs.values,
                  y = top20_orgs.index,
                  orientation='h',
                  color=top20_orgs.values,
                 color_continuous_scale = px.colors.sequential.haline,
                 title= 'Top 20 research Institution by number of prizes')

org_bar.update_layout(xaxis_title='Number of prizes',
                      yaxis_title='Institution',
                      coloraxis_showscale=False)

org_bar.show()


# In[195]:


# Cities with Most Research Centers

top20_org_cities = df.organization_city.value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)

city_bar2 = px.bar(x = top20_org_cities.values,
                   y = top20_org_cities.index,
                   orientation='h',
                   color = top20_org_cities.values,
                   color_continuous_scale=px.colors.sequential.Plasma,
                   title='Which Cities Do the Most Research?')
city_bar2.update_layout(xaxis_title = 'Number of Prizes', 
                        yaxis_title='City',
                        coloraxis_showscale=False)
city_bar2.show()


# In[196]:


# Laurete Birth Cities

top20_cities = df.birth_city.value_counts()[:20]
top20_cities.sort_values(ascending=True, inplace=True)

city_bar = px.bar(x=top20_cities.values,
                  y=top20_cities.index,
                  orientation='h',
                  color=top20_cities.values,
                  color_continuous_scale = px.colors.sequential.Plasma,
                  title = 'Where were the Nobel Laureates Born?')

city_bar.update_layout(xaxis_title = 'Number of Prizes',
                       yaxis_title = 'City of birth',
                       coloraxis_showscale=False)

city_bar.show()


# In[198]:


# The sunburst Chart

country_city_org = df.groupby(['organization_country', 'organization_city', 'organization_name'], as_index=False).agg({'prize':pd.Series.count})

country_city_org = country_city_org.sort_values('prize', ascending=False)

country_city_org 


# In[200]:


burst = px.sunburst(country_city_org,
                    path=['organization_country', 'organization_city', 'organization_name'],
                    values='prize',
                    title='Where do Discoveries Take Place?')

burst.update_layout(xaxis_title='Number of Prizes',
                    yaxis_title='City',
                    coloraxis_showscale=False)

burst.show()


# In[206]:


# Calculate the Age at the Time of Award
birth_years = df.birth_date.dt.year

df['winning_age'] = df.year - birth_years


# In[208]:


df.winning_age.min()


# In[209]:


df[df.winning_age==17.0]


# In[210]:


display(df.nlargest(n=1, columns='winning_age'))
display(df.nsmallest(n=1, columns='winning_age'))


# In[211]:


df.winning_age.describe()


# In[213]:


import seaborn as sns

plt.figure(figsize=(8,4), dpi=200)

sns.histplot(data=df,
            x=df.winning_age,
            bins = 30)

plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')

plt.show()


# In[214]:


plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('whitegrid'):
    sns.regplot(data = df,
                x='year',
                y='winning_age',
                lowess=True,
                scatter_kws = {'alpha':0.4},
                line_kws = {'color':'black'})
    
plt.show()


# In[216]:


plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style('whitegrid'):
    sns.boxplot(data=df,
               x='category',
               y='winning_age')
    
plt.show()


# In[224]:


with sns.axes_style('whitegrid'):
    sns.lmplot(data = df,
               x='year',
               y='winning_age',
               row='category',
               lowess=True,
               aspect=2,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color':'black' })
    
plt.show()


# In[227]:


with sns.axes_style('whitegrid'):
    sns.lmplot(data = df,
               x='year',
               y='winning_age',
               hue='category',
               lowess=True,
               aspect=2,
               scatter_kws = {'alpha': 0.4},
               line_kws = {'linewidth': 5})
    
plt.show()


# In[ ]:




