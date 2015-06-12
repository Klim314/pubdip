#!/usr/bin/env python 3

"""
modfile.py
	Handles python filename renaming/modification
"""

import os

class FileName():
	def __init__(self, fullPath):
		splitPath = os.path.split(fullPath)
		self.path = splitPath[0]

		name  = os.path.splitext(splitPath[1])
		self.baseName = name[0]
		self.ext = name[1]

	def export(self):
		return "".join([self.path, '/', self.baseName, self.ext])

	def modify(self, prefix = '', suffix = ''):
		return "".join([self.path, '/', prefix, self.baseName, suffix, self.ext])

	def modbase(self, prefix = '', suffix = ''):
		return "".join([prefix, self.baseName, suffix])



if __name__ == "__main__":
	temp = FileName("input/tests/SpeciesCount.count.mean_gt50/SpeciesCount.count.mean_gt50_0.pairs")
	print(temp.export())
	print(temp.path)
	print(temp.baseName)
	print(temp.ext)
	print(temp.modify('g1_', "_run10"))

