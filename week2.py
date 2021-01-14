#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[2]:


url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")


# In[3]:


# Get title
title = soup.title
# print(title)

# Get text body
text = soup.get_text()
# print(text)

# Find all the links
all_links = soup.find_all("a")
# for link in all_links:
#     print(link.get("href"))


# In[4]:


# Get data from the rows
rows = soup.find_all('tr')
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)


# In[6]:


df = pd.DataFrame(list_rows)
df1 = df[0].str.split(',', expand=True)
# clean data by removing unnecessary characters
for i in range(len(df1.columns)):
    df1[i] = df1[i].str.strip("\n\r ][")


# In[7]:


# Get column headers
col_labels = soup.find_all("th")
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)


# In[8]:


df2 = pd.DataFrame(all_header)
df3 = df2[0].str.split(',', expand=True)
frames = [df3, df1]

df4 = pd.concat(frames)
df5 = df4.rename(columns=df4.iloc[0])
df6 = df5.dropna(axis=0, how='any')
df7 = df6.drop(df6.index[0])
df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)


# In[9]:


# Data Analysis and Visualization
time_list = df7[' Chip Time'].tolist()
time_list


# In[10]:


# convert 'Chip Time' to minutes
time_mins = []
for i in time_list:
    time = i.split(':')
    if len(time) < 3:
        h,m,s = 0, time[0], time[1]
    else:
        h,m,s = time[0], time[1], time[2]
    math = (int(h) * 3600 + int(m) * 60 + int(s))/60
    time_mins.append(math)
time_mins


# In[11]:


df7['Runner_mins'] = time_mins
df7.head()


# In[12]:


df7.describe(include=[np.number])


# In[13]:


from pylab import rcParams
rcParams['figure.figsize'] = 15, 5
 
df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])


# In[18]:


x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()


# In[21]:


f_fuko = df7.loc[df7[' Gender']=='F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender']=='M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Male')
plt.legend()


# In[22]:


g_stats = df7.groupby(" Gender", as_index=True).describe()
print(g_stats)


# In[24]:


df7.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")


# In[ ]:




