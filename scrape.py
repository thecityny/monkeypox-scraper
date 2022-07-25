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
content=BeautifulSoup(response.content, 'html.parser')

main=content.find("div", {"id":"content"})

main_text=main.find(class_='box').text.strip()

# df=pd.DataFrame(re.findall('\d+\s+\w+\s+\w+', main_text), columns={'cases'})
# df['case_count']=df.cases.str.extract(r'(\w+)').astype(int)
# df['region']=df.cases.str.extract(r'(\w+)$')
# df['region']=df.region.str.replace("New",'NYC')

county_list=[]
for tr in main.find_all('table')[0]:
    county_dict={}
    county_dict['ele']=tr.text.strip()
    county_list.append(county_dict)
    
latest_df=pd.DataFrame(county_list)

new_df=latest_df.ele.str.split("\n", expand=True).dropna().reset_index(drop=True)
new_df.columns=['region', 'case_count']
new_df=new_df.iloc[1:].reset_index(drop=True)
new_df['case_count']=new_df.case_count.str.replace(",","").astype(int)

timestamp=re.findall('As of .* 2022', main_text)[0]
new_df['timestamp']=timestamp
new_df['timestamp']=pd.to_datetime(new_df.timestamp.str.replace("As of ","")).dt.strftime("%Y-%m-%d")

cumulative_cases_all_counties=pd.read_json('data/cumulative_cases_all_counties.json', dtype={'timestamp':str})
cumulative_cases_all_counties=pd.concat([cumulative_cases_all_counties, new_df]).drop_duplicates()

nyc_df=cumulative_cases_all_counties[cumulative_cases_all_counties.region.isin(['Total', 'NYC'])
                                    ].reset_index(drop=True)

nyc_df['timestamp']=pd.to_datetime(nyc_df.timestamp)
nyc_df['daily_cases']=nyc_df.sort_values('timestamp').groupby('region').case_count.diff()
nyc_df['timestamp']=pd.to_datetime(nyc_df.timestamp).dt.strftime("%Y-%m-%d")


new_df.to_json(f'data/monkeypox_{timestamp}.json', orient='records')
cumulative_cases_all_counties.to_json('data/cumulative_cases_all_counties.json', orient='records')
cumulative_cases_all_counties.to_csv('data/cumulative_cases_all_counties.csv', index=False)
nyc_df.to_json('data/all-data.json', orient='records')


# In[2]:


# all_data=pd.read_csv('data/cumulative_cases_all_counties.csv')
# all_data=all_data[~all_data.reporting_date.isin(['July 25 2022'])].reset_index(drop=True)
# all_data=all_data[['timestamp', 'region', 'case_count']]
# cumulative_cases_all_counties=pd.concat([all_data, new_df]).drop_duplicates()
# cumulative_cases_all_counties['region']=cumulative_cases_all_counties['region'].str.replace("orthopoxvirus", 
# 'Total')

# cumulative_cases_all_counties['timestamp']=pd.to_datetime(cumulative_cases_all_counties.timestamp
#                                                          ).dt.strftime("%Y-%m-%d")
# cumulative_cases_all_counties.to_json('data/cumulative_cases_all_counties.json', orient='records')


# In[ ]:




