# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Crunchbase API as a way to track flows between industry and academic work on data
# 
# See [http://developer.crunchbase.com/docs]
# 
# ## To do
# 
# - load the json objects for companies
#     - extract all the people
#     - extract all the tag-list
# - the people - company matrix
# - the tag - company matrix

# <codecell>

import requests
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import json
import StringIO
import time
import graph_tool.all as gt

# <markdowncell>

# ## Queries to get info on companies
# 
# Could just as well do 'people'; 

# <codecell>

query = 'machine-learning&entity=company'

# <codecell>

def get_details(query):
    url = "http://api.crunchbase.com/v/1/search.js?query=" + query + "&api_key=a2gyuj2rmdraphk8k43rbg4g"
    req = requests.get(url)
    res = req.json()
    df = pd.DataFrame.from_dict(res['results'])
    res_count = res['total']
    print('There are %d items' % res_count)
    for page in range(2, (res_count+10//2)//10 + 1):
        try:
            url = "http://api.crunchbase.com/v/1/search.js?query=" + query + "&api_key=a2gyuj2rmdraphk8k43rbg4g&page="+str(page)
            req = requests.get(url)
            res = req.json()
            df = df.append(pd.DataFrame.from_dict(res['results']))
        except Exception, e:
            print(e)
        time.sleep(0.1)
    print('retrieved %d items' % df.shape[0])    
    return df

# <codecell>

ml_company_df = get_details(query)

# <codecell>

bd_company_df = get_details('big-data&entity=company')

# <codecell>

dm_company_df = get_details('data-mining&entity=company')

# <codecell>

pa_company_df = get_details('predictive-analytics&entity=company')

# <codecell>

pr_company_df = get_details('pattern-recognition&entity=company')

# <codecell>

tm_company_df = get_details('text-analytics&entity=company')

# <markdowncell>

# These queries are just a sample, but what is the overall total here?

# <codecell>

company_df = ml_company_df.append([dm_company_df, pa_company_df, bd_company_df, pr_company_df, tm_company_df])
company_df.drop_duplicates(cols = 'permalink', inplace=True)
print(company_df.columns)
company_df.shape

# <codecell>


#company_df.to_csv('company_list.csv', encoding='utf-8')
company_df.category_code.value_counts().plot(kind='barh')

# <markdowncell>

# ## Retrieve info about the companies

# <codecell>

company_names = company_df.name.str.replace(' ', '+')

# <codecell>

entity = 'company'
for company in company_names:
    url = "http://api.crunchbase.com/v/1/"+entity+"/" + company + ".js?api_key=a2gyuj2rmdraphk8k43rbg4g"
    try:
        res = requests.get(url)
        data = res.json()
        json.dump(data, fp=open('data/'+company+'.js', 'w'))
    except Exception, e:
        print e

# <codecell>


data.keys()

# <codecell>


# <markdowncell>

# The tag list offers a way to look at the span of activity and how it is related?

# <codecell>

data['tag_list']

# <markdowncell>

# Relationships are the people -- could build networks here. Could also look at founding data, number of employees, amount of funding, etc

# <codecell>

tags = data['tag_list']
people = data['relationships']
founded_year = data['founded_year']
founded_month = data['founded_month']

# <codecell>

founded_year

# <codecell>

data['relationships']

# <codecell>

query = 'machine-learning&entity=people'
ml_people_df = get_details(query)

# <codecell>

ml_people_df.head()

