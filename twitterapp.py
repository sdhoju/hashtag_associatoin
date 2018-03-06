# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:24:25 2018

@author: Sameer
"""
from __future__ import print_function
import pandas as pd 
import twitter
import time

data = pd.DataFrame(columns=[ 'created_at','id','text','user','source','hashtags'])







def t_api():
    print("In API")
    return twitter.Api(consumer_key='45owJD5G5DDdSsWEAa3TQZCt9',
             consumer_secret='6WyuURska9ByI9zQXLFEDrBZgsn1HrGJ61oU3xyEacnorD9DCQ',
             access_token_key='2988319474-MTtuwJMgl4dZzG6hkjnTZjMNe26xrWm2VVbNVua',
             access_token_secret='W3J6f701MM2UL0eYp8Y6gs3Xrql09EEmPWcMnrdrqjCib'  )

def search(hashtag,start,end,min_id):
    #print("searching for #"+hashtag)
    return api.GetSearch(term=twitter, 
                         raw_query='q=%23'+hashtag+
                         '&count=100&result_type=recent&since='+start+
                         '&until='+end+'&count=100&max_id='+str(min_id))
def min_id(result):
    ids=([r.id for r in result])
    return min(ids)

def panda_data(results):
    for r in results:
        created_at,hashtags,ids,source,text,user = [None]*6
        try:
            created_at = r.created_at
            ids=r.id
            source=r.source
            hashtags = [h.text for h in  r.hashtags]
            text=r.text
            user = r.user.screen_name
            
            i = data.shape[0]
            data.loc[i] = [created_at,ids,text,user,source,hashtags] 
            data.to_csv('data/collected_3_3.csv', encoding='utf-8', index=False)
        except Exception  as e:
            print(e)
            print(str(time.strftime('%X %x %Z')))
            time.sleep(990)
           
    #print("Add to csv file")


def collect_data(hashtag):
    
    results = api.GetSearch(term=twitter, 
                         raw_query='q=%23'+hashtag+
                         '&count=100&result_type=recent&since='+start_date+
                         '&until='+end_date+'&count=100')
    minim = min_id(results)
    panda_data(results)
    for j in range(0,2000):
        
        try:
            print(j)
            results = search(hashtag,start_date,end_date,minim)
            minim = min_id(results)
            panda_data(results)
        except Exception  as e:
            print(e)
            try:
                if(e.message[0]['code']==88):
                    print(str(time.strftime('%X %x %Z')))
                    time.sleep(990)
            except:
                    pass

api=t_api()
start_date='2018-02-26'
end_date='2018-3-04'
print("Start")
collect_data("health")
print("End")