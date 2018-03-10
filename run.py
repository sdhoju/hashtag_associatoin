# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 01:10:40 2018

@author: CREX
"""

import hashtags as hs
import association as asn
import skyline as sky
import time
t0=time.time()

print("Started at ",end="")
print(time.strftime('%X %x'))
print()
#print("Part1: 1 Hashtags are collected from twitterapp.py. \n\t data/collected.csv contains the hashtags collected")
#print("\t2 Comment out line 95 to99 in hashtags.py to collect the data for top 25 hashtags")

hs.main()

asn.main()

sky.main()



print("done in %0.3fs." % (time.time() - t0))
