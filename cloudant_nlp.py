# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:04:04 2019

@author: YIPINL
"""

import os
import pandas as pd
from cloudant import cloudant
os.chdir("C:/NLP_realtime/main")

USERNAME = "xxx
PASSWORD = "xxx"
URL = "xxx"


def df_to_dict(df):
    res = {}
    df['Year'] = df['Year'].apply(lambda x: str(x))
    df['Quarter'] = df['Quarter'].apply(lambda x: str(x))
    year_list = pd.unique(df['Year']).tolist()
    for year in year_list:
        temp1 = df[df['Year'] == year]
        res[year] = {}
        quarter_list = pd.unique(temp1['Quarter']).tolist()
        for quarter in quarter_list:
            temp2 = temp1[temp1['Quarter'] == quarter]
            res[year][quarter] = {}
            category_list = pd.unique(temp2['Category']).tolist()
            for category in category_list:
                temp3 = temp2[temp2['Category'] == category]
                res[year][quarter][category] = {}
                subcategory_list = pd.unique(temp3['Subcategory']).tolist()
                for subcategory in subcategory_list:
                    temp4 = temp3[temp3['Subcategory'] == subcategory].reset_index(drop = True)
                    res[year][quarter][category][subcategory] = {}
                    for i in range(len(temp4)):
                        topic = temp4.loc[i, 'Content']
                        weight = temp4.loc[i, 'Weight']
                        number = temp4.loc[i, 'Number']
                        res[year][quarter][category][subcategory][topic] = {}
                        res[year][quarter][category][subcategory][topic]['weight'] = float(weight)
                        res[year][quarter][category][subcategory][topic]['number'] = int(number)
    return res
                    
df = pd.read_csv("Topic_modeling_result.csv")
res = df_to_dict(df)

a = df.set_index(['Year','Quarter']).T.to_dict('list')
a = df.to_dict()
with cloudant(USERNAME, PASSWORD, url=URL) as client:

    ## Perform client tasks...
    #session = client.session()
    #print('Username: {0}'.format(session['userCtx']['name']))
    #print('Databases: {0}'.format(client.all_dbs()))

    # Create a database
    #topic = client.create_database('topic')
    #if topic.exists():
        #print('SUCCESS!!')

    # You can open an existing database


    # Create a document using the Database API
    my_database = client['topic']
    
    print(my_database['yipin'])
    #my_document = my_database.create_document(a)
    
    del my_database
    my_database = client['my_database']


    
    a = res['2018']['1']["Bank's Business Applications"]\
    ['Concur']['bank business application']
    json.dumps(res)
    type(a['number'])



    a = {'_id': 'yipin','data': res}

















session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))




selector = {
	'type': 'example_doc'
}

result = connection.get_database().get_query_result(selector)
for r in result:
	print(r)









session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))


# Adding document to cloudant
document = {
	'type': 'example_doc',
	'date': '02/01/2019'
}
connection.save(document)

# Selecting Documents
selector = {
	'type': 'example_doc'
}

result = connection.get_database().get_query_result(selector)
for r in result:
	print(r)