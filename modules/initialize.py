#!/usr/bin/env python3
"""
initialize.py
	loads the pubdip.ini file
	returns a dictionary containing all terms
"""

def execute(target):
	res = dict()
	with open(target) as f:
		for i in f:
			if i[0] == '#':
				continue
			temp = i.split('=')
			res[temp[0]] = temp[1].strip()
	return res


if __name__ == "__main__":
	path = "../pubdip.ini"
	print(execute(path))
