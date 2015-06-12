#!/usr/bin/env python
"""
pairpapersum.py
	Sums paper count of all species 2-pairs. Takes in either raw count or twocount data from pubdip
"""

def execute(target, twocount = 0):
	holder = []
	with open(target) as f:
		for i in f:
			#settle comments
			if i[0] == "#":
				continue
			else:
				holder.append(i.strip().split('\t'))
	if twocount == 0:
		splat = [holder[i*6] for i in range(len(holder)//6)]
	else:
		splat = [i for i in holder]
	splatInt = [int(i[2]) for i in splat]
	total = sum(splatInt)
	return total


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("target", help= "Paper count data file from pubdip", default = "input/pattern/")
	parser.add_argument("-t", "--twocount", help = "twocount file flag if input is a twocount file", action = "store_true", default = False)
	args = parser.parse_args()

	print(execute(args.target, args.twocount))

