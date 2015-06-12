#!/usr/bin/env python3

import sys

target = sys.argv[1]
total = 0
with open(target) as f:
	for i in f:
		if i == "\n" or i[0] == '#':
			continue
		else:	
			try:
				total += int(i.strip().split('\t')[-1])
			except:
				print("ERROR: ", [i])
				raise

print("SUM IS: ", str(total))
