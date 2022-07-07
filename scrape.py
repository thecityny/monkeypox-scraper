#!/usr/bin/env python
# coding: utf-8

# text structure: As of July 6, 2022, a total of 128 confirmed orthopoxvirus/monkeypox cases-a designation established by the Centers for Disease Control and Prevention (CDC)-have been identified with 119 in New York City, 5 in Westchester County, 
# 1 in Sullivan County, 1 in Chemung County, 1 in Rockland County and 1 in Suffolk County.

# In[1]:


import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

url='https://health.ny.gov/diseases/communicable/zoonoses/monkeypox/'
response=requests.get(url)
content=BeautifulSoup(response.content)

main=content.find("div", {"id":"content"})

main_text=main.find(class_='box').text.strip()

reporting_date=re.search('As of\s+\w+\s+\d+,\s+\d{4}', main_text)[0]
df=pd.DataFrame(re.findall('\d+\s+\w+\s+\w+', main_text), columns={'cases'})
df['case_count']=df.cases.str.extract(r'(\w+)').astype(int)
df['region']=df.cases.str.extract(r'(\w+)$')
df['region']=df.region.str.replace("New",'NYC')
df['reporting_date']=re.search('As of\s+\w+\s+\d+,\s+\d{4}', main_text)[0]
df['reporting_date']=df.reporting_date.str.replace("As of ","")
df=df[['reporting_date', 'region', 'case_count', 'cases']]

df.to_csv(f'data/monkeypox_cases_{reporting_date}.csv', index=False)

