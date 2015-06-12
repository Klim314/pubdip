#!/usr/bin/env python3 

"""
fileSplit.py
	Takes a txt and splits it into n equal parts+
"""

import sys
import os
from math import ceil

target = sys.argv[1]
n = int(sys.argv[2])
split = os.path.splitext(target)
filename, filepath = split[0], split[1]
filename = os.path.split(filename)
dirname, filename = filename[0], filename[1]
print(dirname)
print(filename)
print(filepath)
with open(target) as f:
	holder = [i for i in f]

chunk = len(holder)//n

split = [holder[i:i+chunk] for i in range(0,len(holder), chunk)]

if not os.path.exists(dirname + '/' + filename + "/"):
	print("making: ", dirname + '/' + filename + "/" )
	os.makedirs(dirname + '/' + filename + "/")

for num, lst in enumerate(split):
	with open(dirname + '/' + filename + '/' + filename+ "_" + str(num) + filepath, 'w') as f:
		for i in lst:
			f.write(i)
