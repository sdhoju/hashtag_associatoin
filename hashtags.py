# -*- coding: utf-8 -*-
#import re
import time
import csv
#import itertools
import re
import twitterapp as tw

t0=time.time()

print("Started at ",end="")
print(time.strftime('%X %x'))



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

def get_pair(sorted_hashtags):
    good_hash=[]
    list_of_2_hash=[]
    for key, value in sorted_hashtags.items():
        if (value>item_threshold):
            good_hash.append(key)
    for i in range(0,len(good_hash)):
        for j in range(i,len(good_hash)):
            if good_hash[i]!=good_hash[j]:
                list_of_2_hash.append([good_hash[i],good_hash[j]])
    return list_of_2_hash

def get_list_2items(phase_2,main_list):
    two_tup=[]
    for h in phase_2: 
        two_tup.append(get_support(h,main_list))
    #return support of that item
    return two_tup

def get_triplets(two_tup):
    good_list=[]
    list_of_3=[]
    for i in range(0,len(two_tup)):
        if (two_tup[i][1]>teir2_threshold):
            good_list.append(two_tup[i][0])
    for i in range(0,len(good_list)):
        for j in range(i,len(good_list)):
            if good_list[i][0]==good_list[j][0] and good_list[i] !=good_list[j]:
                list_of_3.append(list(set(good_list[i]+good_list[j])))
    return list_of_3


def get_support(check_list,main_list):
    support=0
    for m in main_list:
        if set(check_list).issubset(m):
            support+=1
    #return support of that item
    return (check_list,support)

def main():
#    users=load_users("collected.csv")
#    top_users=get_sorted(users,50)
#    print(top_users)
#    
    list_hashtags=load_data("collected.csv")
    hashtags=all_hashtags(list_hashtags)
    top_hashtags=get_sorted(hashtags,25)
    
    for key in top_hashtags:
#        print(key)
        top_hashtags.pop(key)
        break
    for key in top_hashtags:
#        print(key)
        tw.collect_data(key)
        
    
#    rh1=load_data("collected.csv")
#    rh2=load_data("temp.csv")
#    main_list=rh1+rh2
#    main_list.sort()
#    list(main_list for main_list,_ in itertools.groupby(main_list))  #removing the duplicate hashtags
#    
#    
#    data=all_hashtags(main_list)
# 
#    sorted_hashtags=get_sorted(data)
#    phase_2=get_pair(sorted_hashtags)
##    print(phase_2)
#    list_3=get_list_2items(phase_2,main_list)
#    phase_3=get_triplets(list_3)
#    for h in phase_3: 
#        print(get_support(h,main_list))
        
#    print(main_list)
    

main()


print("done in %0.3fs." % (time.time() - t0))


















