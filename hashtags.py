# -*- coding: utf-8 -*-
#import re
import time
import csv
import re
import twitterapp as tw
import pickle 
import itertools
t0=time.time()

#print("Started at ",end="")
#print(time.strftime('%X %x'))



#import twitterapp
item_threshold=500
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
#                row[5]=re.sub(r'[^\x00-\x7f]',r'',row[5]) 
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
                data.append(i.lower())
    return data

#take the filename and gives the list of users 
def load_users(filename):
    file="data/"+filename
    users=[]
    
    with open(file,encoding="latin-1") as f:
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader:
            text = row[2]
            if text.find('RT') ==-1:    
                users.append(row[3])            
    return users

def get_sorted(data,max_output=_NO_DEFAULT):
    from collections import Counter
    no_items=None
    if max_output!=_NO_DEFAULT:
        no_items=max_output
    counts = Counter(data)
    sort_data=dict(counts.most_common(no_items))                         #Get the sorted  hashtags in Dictionary 
#    return sorted (counts, key=counts.get, reverse=True)[:max_output]
    return sort_data
def main():
    list_hashtags=pickle.load(open("data/main_list.pickle", "rb"))
    list(list_hashtags for list_hashtags,_ in itertools.groupby(list_hashtags))  #removing the duplicate hashtags
    
    count=0
    for l in range(0,len(list_hashtags)):
        if len(list_hashtags[l][0])>1:
            print(list_hashtags[l])
            count+=1
        if count==10:
            break
    print()
#    list_hashtags=load_data("collected.csv")                # for getting list os hashtags  
    hashtags=all_hashtags(list_hashtags)
    top_hashtags=get_sorted(hashtags,50)
    print("Top Hashtags excluding Health are: ")
    for key,value in top_hashtags.items():
        print(key, end=": ")
        print(value)
    print()
    users=load_users("collected.csv")
    top_users=get_sorted(users,50)
    
    print("Top Users are: ")
    for key,value in top_users.items():
        print(key, end=": ")
        print(value)
    print()

    # for collecting data from twitter api
    '''
    top25_hashtags=get_sorted(hashtags,25)
    for key in top25_hashtags:
        print(key)
        tw.collect_data(key)
    '''

#main()


#print("done in %0.3fs." % (time.time() - t0))


















