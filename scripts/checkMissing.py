#!/usr/bin/env python3

"""
checkMissing
"""

import sys
import csv
import os
targetFile = sys.argv[1]

refFile = sys.argv[2]

outFile = os.path.split(refFile)
outFile = outFile[0] + "/MISSING_" + outFile[1]

print(outFile)

ref = set()
with open(refFile ) as f:
	fIn = csv.reader(f, delimiter = '\t')

	for i in fIn:
		ref.add(" ".join(i[:2]))

with open(targetFile) as f:
	with open(outFile, 'w') as w:
		fIn = csv.reader(f, delimiter = '\t')

		for i in fIn:
			if " ".join(i[:2]) not in ref:
				w.write("\t".join(i[:2])+'\n')

