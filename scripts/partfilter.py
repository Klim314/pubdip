#!/usr/bin/env python3
"""
partfilter.py:
	takes in a tsv, filters tsv by line if a entry for a designated column is 0

"""
import csv

def readTSV(target):
	holder = []
	with open(target) as f:
		tsvin = csv.reader(f, delimiter = '\t')

		for i in tsvin:
			holder.append(i)
	return holder


def partFilter(fileLst, col):
	holder = []
	for i in fileLst:
		if i[col] != '0':
			holder.append(i)
	return holder


if __name__ == "__main__":
	import argparse
	import sys
	import os

	parser = argparse.ArgumentParser()
	parser.add_argument("target", help = "Target file. File must be a line-separated list of tab separated term terms")
	parser.add_argument("column", help = "Choose column to filter by")
	parser.add_argument("-o", "--output", help = "override output name")
	parser.add_argument("-d", "--debug", action = "store_true", default = False, help = "Enable debug mode")
	args = parser.parse_args()

	if args.output:
		outFile = args.output
	else:
		inFile = args.target
		splitPath = os.path.split(args.target)
		outDir = "output/"
		fileName = splitPath[1]
		outFile = outDir + "filtered_" + fileName

	if args.debug:
		inFile = "../output/2015-05-28-14_30_SUM_parts.out"
	
	read = readTSV(inFile)
	filtered = partFilter(read, 2)
	with open(outFile, 'w') as f:
		for i in filtered:
			f.write('\t'.join(i) + '\n')
