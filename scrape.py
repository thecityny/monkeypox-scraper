#!/usr/bin/env python
# coding: utf-8

# text structure: As of July 6, 2022, a total of 128 confirmed orthopoxvirus/monkeypox cases-a designation established by the Centers for Disease Control and Prevention (CDC)-have been identified with 119 in New York City, 5 in Westchester County, 
# 1 in Sullivan County, 1 in Chemung County, 1 in Rockland County and 1 in Suffolk County.

# In[13]:


import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

url='https://health.ny.gov/diseases/communicable/zoonoses/monkeypox/'
response=requests.get(url)
content=BeautifulSoup(response.content, 'html.parser')

main=content.find("div", {"id":"content"})

main_text=main.find(class_='box').text.strip()

df=pd.DataFrame(re.findall('\d+\s+\w+\s+\w+', main_text), columns={'cases'})
df['case_count']=df.cases.str.extract(r'(\w+)').astype(int)
df['region']=df.cases.str.extract(r'(\w+)$')
df['region']=df.region.str.replace("New",'NYC')

reporting_date=re.findall('As of .* 2022', main_text)[0]
df['reporting_date']=reporting_date

df['reporting_date']=df.reporting_date.str.replace("As of ","")
df=df[['reporting_date', 'region', 'case_count', 'cases']]
df['timestamp']=pd.to_datetime(df['reporting_date'])


df.to_json(f'data/monkeypox_{reporting_date}.json', orient='records')

all_data=pd.read_json('data/all-data.json')
merged_df=pd.concat([all_data, df], ignore_index=True).drop_duplicates()

merged_df['timestamp']=pd.to_datetime(merged_df['reporting_date']).dt.strftime("%Y-%m-%d")


merged_df.to_csv('data/all-data.csv', index=False)
merged_df.to_json('data/all-data.json', orient='records')



# In[2]:


# pd.concat([pd.read_csv('data/july6.csv'),pd.read_csv('data/july7.csv')], ignore_index=True).to_csv(
#     'data/all-data.csv', index=False)


# In[12]:


merged_df.info()


# In[ ]:




