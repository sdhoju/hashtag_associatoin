# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 23:40:09 2018

@author: Sameer
"""
import re
import csv
def load_data(filename):
    file="data/"+filename
    
    import ast
    data=[]
   
    with open(file,encoding="utf8") as f:
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader[:20]:
            for i  in (ast.literal_eval(row[5])):
                if (i.lower()!='health'):
                    data.append(i.lower())
#            print(row[4])
    return data
def load_users(filename):
    file="data/"+filename
    users=[]
    with open(file,encoding="utf8") as f:
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader:
            users.append(row[4])
#            for i  in (ast.literal_eval(row[4])):
#                if (i.lower()!='health'):
#                    
    return users


def get_sorted(data,max_output):
    from collections import Counter
    counts = Counter(data)
#    print(counts.most_common)
    return sorted (counts, key=counts.get, reverse=True)[:max_output]

def load_data1(filename):
    file="data/"+filename
    import csv
    import ast
    data=[]
    with open(file,encoding="utf8") as f:
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader:
            un=(ast.literal_eval('"'+row[6]+'"').split(","))
            for u in un:
                try:
                    s=(u.replace("Hashtag(Text='", ""))
                    s=re.sub(r'\W+', '', s)
                    if(s.lower()!='health' and len(s)>0):
                        data.append(s.lower())
                except:
                    pass
    return data

data=load_data("collected.csv")
users= load_users("tweets_1.csv")
top_users=get_sorted(users,50)
top_hashtags=get_sorted(data,50)


print("Top users are:")
for u in top_users:
    print(u , end=" ")
print("\n")
print("Top hashtags are:")
for h in top_hashtags:
    print(h , end=", ")
#for h in tocollect:
#    print(h)
