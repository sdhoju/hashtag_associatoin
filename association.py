    # -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 15:07:23 2018

@author: CREX
"""

# -*- coding: utf-8 -*-
#import re
import pickle
import time
import csv
import itertools
import re
import pandas as pd 
from collections import Counter


t1=time.time()

print("Started at ",end="")
print(time.strftime('%X %x'))

#import twitterapp
item_threshold=3000
teir2_threshold=80
    



class _NO_DEFAULT:
    def __repr__(self):return "<no default>"
_NO_DEFAULT = _NO_DEFAULT()

#Reads csv file and returns the list of list of hashtags in that file
def load_data(filename):
    import ast
    file="data/"+filename
    list_of_hashtags=[]
    with open(file,encoding="latin-1") as f:                       
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader:
            try:
                row[5]=re.sub(r'[^\x00-\x7f]',r'',row[5]) 
                rows_hashtags=ast.literal_eval(row[5]) #Convert String in list form to list
                text = row[2]
                if text.find('RT') ==-1 and len(rows_hashtags)>0:                #Remove Retweets
                    list_of_hashtags.append(rows_hashtags)      
            except:
                pass
    return list_of_hashtags

#take the list of list of hashtags and return list of all hashtags
def all_hashtags(rows_hashtags):
    data=[]
    for row_hastag in rows_hashtags:
        for i  in row_hastag:           #Convert String in list form to list
            if (i.lower()!='health')and len(i)>0:
#            if len(i)>0:
                data.append(i.lower())
    print("Total of %d hashtags"%(len(data)))
    return data

#take the filename and gives the list of users 
def load_users(filename):
    file="data/"+filename
    users=[]
    with open(file,encoding="latin-1") as f:
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader:
            users.append(row[3])            
    return users


def get_sorted(data,max_output=_NO_DEFAULT):
    no_items=None
    if max_output!=_NO_DEFAULT:
        no_items=max_output
    counts = Counter(data)
    sort_data=dict(counts.most_common(no_items))                         #Get the sorted  hashtags in Dictionary 
#    return sorted (counts, key=counts.get, reverse=True)[:max_output]
    print("%d unique hashtags"%(len(sort_data)))
    return sort_data

def get_pair(sorted_hashtags):
    good_hash=[]
    list_of_2_hash=[]
    print("Pruning on frequency %d" %item_threshold)
    for key, value in sorted_hashtags.items():
        if (value>item_threshold):
            good_hash.append(key)
        
    for i in range(0,len(good_hash)):
        for j in range(i,len(good_hash)):
            if good_hash[i]!=good_hash[j]:
                list_of_2_hash.append([good_hash[i],good_hash[j]])
#    list_of_2_hash=sorted(list_of_2_hash)
    return list_of_2_hash

def get_all_tuples(alist):
    tup=[]
    for h in alist: 
        tup.append(get_support(h))
    #return support of that item
    return tup

#given a tuple of (list and count), it return the list of K+1 frequent items 
def add_dimension(tup):
    add_list=[] 
    for i in range(0,len(tup)):
        for j in range(i,len(tup)):
            if(len(set(tup[i][0]).union(tup[j][0]))==len(tup[i][0])+1):
                add_list.append(list(set(tup[i][0]).union(tup[j][0])))
    add_list=sorted(add_list)
    new_k = []
    for elem in add_list:
        if elem not in new_k:
            new_k.append(elem)
    add_list=new_k
    return add_list

#return support of that item given list and mainlist
def get_support(check_list):
    support=0
    for m in main_list:
        if set(check_list).issubset(m):
            support+=1
#        else:
#            reduced_list.remove(m)
    return (check_list,support)

def get_confidence(list_I,hashtag):
    s=get_support(list_I)[1]
    i=list_I
    i.append(hashtag)
    s_union=get_support(i)[1]
    i.remove(hashtag)
    try:
        confidence=s_union/s
    except ZeroDivisionError:
        confidence=0
    return confidence

def get_prob(hashtag):
    count=0
    for m in main_list:
        if hashtag in m:
            count+=1
    return count/len(main_list)


def get_interest(list_I,hashtag):
    interest=abs(get_confidence(list_I,hashtag)-get_prob(hashtag))
    return interest

def get_conviction(list_I,hashtag):
    try:
        conviction= (1-get_support([hashtag])[1]/len(main_list))/(1-get_confidence(list_I,hashtag))
    except:
        conviction=0
    return conviction

def prune(tup,threshold):
    c=len(tup)
    good_list=[]
    for i in range(0,len(tup)):
        if (tup[i][1]>threshold):
            good_list.append(tup[i])
    print("Prunned form %d to %d on frequency %d" %(c,len(good_list),threshold))
    return good_list
    
def have_all(alist,hashtag):
 
#    support=get_support(alist,main_list)[1]/len(main_list)
    conf=get_confidence(alist,hashtag)
    inter= get_interest(alist,hashtag)
    conv=get_conviction(alist,hashtag)
    
    return (alist,conf,inter,conv)
def reduce_list(alist):
    rl=[]
    rl=alist
    return rl
def save_datagram(tup):
    filename=str(len(tup))
    dat = pd.DataFrame(columns=[ 'List','Confidence','Interest','Conv']) 
    for p in tup:
        dt=(have_all(p,"health"))
        i = dat.shape[0]
        dat.loc[i] = [dt[0],dt[1],dt[2],dt[3]]
        dat.to_csv('data/skyline'+filename+'.csv', encoding='utf-8', index=False)
def sort(tup):
    tup.sort(key=lambda x: x[1],reverse=True)

def main():
    
    data=all_hashtags(main_list)
    sorted_hashtags=get_sorted(data)
    print()
    
    print("Examples of generated Singles")
    for key in list(sorted_hashtags.items())[:10]:
        print(key)
    print()
#    print(sorted_hashtags)
    
    #to generate tuple of on raw data
    """
    t0=time.time()
    pair=get_pair(sorted_hashtags)
    print("Pairs Generated in %0.3fs." % (time.time() - t0))
    pair_tuple=get_all_tuples(pair)
    p_pair_tuple=(prune(pair_tuple,500))
    pickle.dump(p_pair_tuple, open("data/pair_tup.pickle", "wb"))

    """
    p_pair_tuple=pickle.load(open("data/pair_tup.pickle", "rb"))
    sort(p_pair_tuple)
    print("Example of generated pair tuple")
    for p in p_pair_tuple[:10]:
        print(p)
    print()
    
    #to generate tuple of on raw data
    '''
    t0=time.time()
    triplets=add_dimension(p_pair_tuple)
    print("triplets Generated in %0.3fs." % (time.time() - t0))
    triplets_tup=get_all_tuples(triplets)
    triplets_tup=prune(triplets_tup,500)
    pickle.dump(triplets_tup, open("data/trip_tup.pickle", "wb"))
    ''' 
#    
#
#    
    
#     import operator
    trip=pickle.load(open("data/trip_tup.pickle", "rb"))
#    trip.sort(key=operator.itemgetter(1),reverse=True)
    sort(trip)
    print("Examples of generated triplets tuple")
    for t in trip[:10]:
         print(t)
    print()
    '''
    t0=time.time()
    quad=add_dimension(trip)
    quad_tup=get_all_tuples(quad)
    quad_tup=prune(quad_tup,500)
    pickle.dump(quad_tup, open("data/quad.pickle", "wb"))
    print("Quad Generated in %0.3fs." % (time.time() - t0))
    '''
    quadd=pickle.load(open("data/quad.pickle", "rb"))
    print("Examples of generated Quadra tuple")
    sort(quadd)
    for t in quadd[:10]:
         print(t)
    print()
    
    '''
    t0=time.time()  
    penta=add_dimension(quadd)
    penta_tup=get_all_tuples(penta)
    penta_tup=prune(penta_tup,500)
    pickle.dump(penta_tup, open("data/penta_tup.pickle", "wb"))
    print("Penta Generated in %0.3fs." % (time.time() - t0))
    '''
    penta=pickle.load(open("data/penta_tup.pickle", "rb"))
    print("Examples of generated Penta tuple")
    sort(penta)
    for t in penta[:10]:
         print(t)
    print()

#To get the list of Hashtag from raw data
'''
#rh1=load_data("collected.csv")
#rh2=load_data("Top_25.csv")
#main_list=rh1+rh2
#main_list.sort()
#list(main_list for main_list,_ in itertools.groupby(main_list))  #removing the duplicate hashtags
#pickle.dump(main_list, open("data/main_list.pickle", "wb"))
'''

main_list=pickle.load(open("data/main_list.pickle", "rb"))
main()

print("done in %0.3fs." % (time.time() - t1))


















