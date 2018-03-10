# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:59:14 2018

@author: CREX
"""

#import association as asn
import csv
import ast
import time
t0=time.time()
import itertools

print("Started at ",end="")
print(time.strftime('%X %x'))
file="data/skyline50.csv"

def load_data():
    data=[]
    with open(file,encoding="latin-1") as f:                       
        reader = list(csv.reader(f))
        reader.pop(0)
        data=reader
        for d in data:
            d[0]=ast.literal_eval(d[0])
            d[1]=ast.literal_eval(d[1])
            d[2]=ast.literal_eval(d[2])
            d[3]=ast.literal_eval(d[3])
            d[1]=[d[1],d[2],d[3]]
    return data

def add_dimention(data):
    num=len(data[0][0])+1
#    print(data[0][1][1])
    new_data=[]
    add=[]
    mins=[]

    for i in range(0,len(data)):
         for j in range(i+1,len(data)):
            data[i][0].sort()
            if(len(set(data[i][0]).union(data[j][0]))==num):
                add=( list(set(data[i][0]).union(data[j][0])))
                mins.append(min(data[i][1][0],data[j][1][0]))
                mins.append(min(data[i][1][1],data[j][1][1]))
                mins.append(min(data[i][1][2],data[j][1][2]))
                new_data.append([add,mins])
                add=[]
                mins=[]
                
    new_k = []
    for elem in new_data:
        if elem not in new_k:
            new_k.append(elem)
    new_data=new_k
#    new_data=list(set(new_data))        
    return new_data

def prune(data,threshold):
    d=[]
    l=len(data)
    for p in data:
        if(not(p[1][0]<threshold or p[1][1]<threshold  or p[1][2]<1 )):
            d.append(p)
    print("Prunned from %d to %d" %(l,len(d)))
    return d



def print_list(data):
    d=data.copy()
    list(d for d,_ in itertools.groupby(d))
    for p in d:
       print(p[0],end=" ->  ")
       print("Confidence: %3f, Interst: %3f, Conviction: %3f"%(p[1][0],p[1][1],p[1][2]))
    print()
   
def sort_by_conv(data):
    d=data.copy()
    d.sort(key=lambda x: x[1][2],reverse=True)
    return d

def main():
    try:
        single=load_data()
        pruned_data= prune(single,0.25)
        sort_by_conv(pruned_data)
        print_list(pruned_data)
    
    
        pair = add_dimention(pruned_data)
        pr_pair=prune(pair,0.35)
        sort_by_conv(pr_pair)
        print_list(pr_pair)

        trip=add_dimention(pair)
        trip=prune(trip,0.32)
        sort_by_conv(trip)
        print_list(trip)
        #
        quad=add_dimention(trip)
        quad= prune(quad,0.322)
        sort_by_conv(quad)
        print_list(quad)
        
        penta=add_dimention(quad)
        penta= prune(penta,0)
        sort_by_conv(penta)
        print_list(penta)
        
    except IndexError:
        print("No possible list were created")
    #
#    #quad=trip
#    penta=add_dimention(quad)
#    prune(penta,0.99)
#    sort_by_conv(penta)
#    print_list(penta)
main()
print("done in %0.3fs." % (time.time() - t0))
