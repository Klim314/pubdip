#!/usr/bin/env python 3

def loadAnn(target):
	ann = []
	with open(target) as f:
		for i in f:
			ann.append(i.strip())
	split = []
	for i in range(0, len(ann), 3):
		try:
			split.append((ann[i], ann[i+1], ann[i+2]))
			if ann[i][0] not in ["@", ">", "?"]:#quick debug hardcode
				print(ann[i-3:i+3])
				print(ann[i])
				raise Exception("Missing Padding. File blocks of uneven size")
		except:
			#print(ann[i-1:])
			raise


	return split

def eva(inp, ann, u = 0, logging = 0):
	total = len(inp)
	correct = 0
	TP = 0
	FP = 0
	FN = 0

	#Keep track of index
	count = 0

	if logging:
		print("LOGGING")
		fpLog, fnLog, tpLog = [],[], []

	for i,j in zip(inp, ann ):
		#print(i, j[0][1] )
		try:
			if u == True and (j[0][0] == "?" or j[0][0] == "@"):
				count +=1
				total -=1
				continue
			if i == j[0][1]:
				if i == "T":
					TP += 1
					if logging:
						tpLog.append(str(count) + " " +  str(j))
				correct += 1
			else:
				if i == "T":
					FP += 1
					if logging:
						fpLog.append(j)
				if i == "F":
					FN += 1
					if logging:
						fnLog.append(j)
			count +=1

		except:
			print("i :", i)
			print("j :", j)
			raise

	print("Total samples analyzed:", total)
	print("Correctly Assigned: ", correct)
	print("True Positives: ", TP)
	print("True Negatives: ", correct - TP)
	print("False Positives: ", FP)
	print("False Negatives: ", FN)
	if logging:
		with open(logging + ".log", 'w') as f:
			f.write("TRUE POSITIVES:\n")
			for i in tpLog:
				f.write(str(i) + '\n\n')

			f.write("FALSE POSITIVES:\n")
			for i in fpLog:
				f.write(str(i) + '\n\n')

			f.write("FALSE NEGATIVES:\n")
			for i in fnLog:
				f.write(str(i) + '\n\n')
	return TP
def evaluate(inp, annPath, u = 0, logging = None):
	return( eva(inp,loadAnn(annPath), u = u, logging = logging))



if __name__ == "__main__":
	a = "annotated/lactobacillus_acidophilus#escherichia_coli.ann"
	b = loadAnn(a)
	print(len(b))

	#print(a)
	testresults = ['T', 'T', 'F', 'F', 'T', 'T', 'T', 'T', 'F', 'F', 'T', 'F', 'T', 'T', 'F', 'T', 'T', 'F', 'F', 'T', 'T', 'F', 'T', 'F', 'T', 'F', 'T', 'F', 'F', 'F']

	print("BEGINNING")
	evaluate(testresults, "annotated/lactobacillus_acidophilus#escherichia_coli.ann", "testlog")



#eva(testresults, a, logging = "testlog")*