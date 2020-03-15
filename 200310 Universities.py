#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data


# In[2]:


#Load datasets
diversity = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/diversity_school.csv')
cost = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/tuition_cost.csv')


# In[3]:


priciest50 = cost.sort_values(by=['in_state_total'], ascending=False)[:50].name
cheapest50 = cost.sort_values(by=['in_state_total'], ascending=True)[:50].name


# In[4]:


categories = ["White","Black", "Hispanic", "Asian", "American Indian / Alaska Native", "Native Hawaiian / Pacific Islander"]


# In[5]:


df2 = diversity[(diversity.category.isin(categories))& diversity.name.isin(priciest50)]
df4 = diversity[(diversity.category.isin(categories))& diversity.name.isin(cheapest50)]


# In[6]:


df3 = df2.loc[:, df2.columns != 'total_enrollment']

df3 = df3.pivot(columns='category', values='enrollment', index='name')

df3 = df3.assign(sum=df3.apply(np.sum, axis=1)).reset_index()

df3 = df3.melt(id_vars=['name','sum']).sort_values(by='name')

df3 = df3.assign(prop=lambda x: x.value/x['sum']*100)


# In[7]:


df5 = df4.loc[:, df2.columns != 'total_enrollment']

df5 = df5.pivot(columns='category', values='enrollment', index='name')

df5 = df5.assign(sum=df5.apply(np.sum, axis=1)).reset_index()

df5 = df5.melt(id_vars=['name','sum']).sort_values(by='name')

df5 = df5.assign(prop=lambda x: x.value/x['sum']*100)


# In[8]:


pricy_order = df3[df3.category=='White'].sort_values(by=['prop'],ascending=False).name
cheapy_order = df5[df5.category=='White'].sort_values(by=['prop'],ascending=False).name


# In[24]:


expensive_chart = alt.Chart(df3).mark_bar().encode(
    alt.X('sum(value)',stack='normalize',title=''),
    alt.Y('name', sort=list(pricy_order),title='University'),
    color = 'category'
).properties(width = 200, height=800)

cheap_chart = alt.Chart(df5).mark_bar().encode(
    alt.X('sum(value)',stack='normalize',title=''),
    alt.Y('name', sort=list(cheapy_order),title='University'),
    color = 'category'
).properties(width = 200, height=800)

#Unify for final plot
alt.hconcat(expensive_chart, cheap_chart)


# In[10]:


#Another way to do the plot
alt.Chart(df3).mark_bar().encode(
    alt.X('prop', stack = 'zero',scale=alt.Scale(domain=(0, 100))),
    alt.Y('name',sort=list(pricy_order)),
    color='category'
)


# In[ ]:




