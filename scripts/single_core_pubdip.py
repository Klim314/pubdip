#!/usr/bin/env python3

import sys

target = sys.argv[1]
total = 0
with open(target) as f:
	for i in f:
		total += int(i.strip().split('\t')[-1])

print("SUM IS: ", i)
