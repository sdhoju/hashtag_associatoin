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

def min_date(result):
    dates=([r.created_at for r in result])
    min_date= min(dates).lower().split(" ")
    date="2018-"
    if (min_date[1]=='feb'):
        date+="02-"
    elif(min_date[1]=='mar'):
        date+="03-"
    else:
         date+="02"
    date+=min_date[2]
    return date

def panda_data(results):
    for r in results:
        created_at,hashtags,ids,source,text,user = [None]*6
        
        text=r.text
        if (text[:2]!="RT") and r.lang!="en":
            created_at = r.created_at
            ids=r.id
            source=r.source
            hashtags = [h.text for h in  r.hashtags]
            user = r.user.screen_name
            i = data.shape[0]
            data.loc[i] = [created_at,ids,text,user,source,hashtags] 
            data.to_csv('data/topasd_25.csv', encoding='utf-8', index=False)


def collect_data(hashtag):
    results = api.GetSearch(term=twitter, 
                         raw_query='q=%23'+hashtag+
                         '&count=100&result_type=recent&since='+start_date+
                         '&until='+end_date+'&count=100')
    minim = min_id(results)
    end=(min_date(results))
    count=1
    while(end!=start_date):  
        try:
            results = search(hashtag,start_date,end_date,minim)
            minim = min_id(results)
            end=(min_date(results))
            count+=1
            if(count%25==0):
                print(hashtag)
            panda_data(results)
        except Exception  as e:
            count=1
            print(e)
            try:
                if(e.message[0]['code']==88):
                    print(str(time.strftime('%X %x %Z')))
                    time.sleep(990)
            except:
                    pass

api=t_api()
start_date='2018-03-05'
end_date='2018-03-7'

#print("Start")
##collect_data("health")
#print("End")