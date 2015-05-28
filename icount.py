#!/usr/bin/env python3
"""
icount:
	Coarse filter system for inhibitory relationships
	Analyzes abstracts on a sentence by sentence basis searching for two stipulated terms and a 
	set of negative terms.
	
	Object A and B are each two letter names defined in the file name as follows
		OBJECT_A#OBJECT_B
	
	returns a total number of hits which contain the two terms and a negative term in the same sentence
"""
#NOTE: Grab pre/proceeding sentences as well. Context

import nltk
import os
from segtok.segmenter import split_single as ssplit
import sent_tokenize as st
import evaluate


#////////////////////////
#INITIAL SETUP
#////////////////////////
if not os.path.exists("output/abcheck"):
	os.mkdir("output/abcheck")

outdir = "output/abcheck/"
-
"""
Negative terms and stemmer system
"""
unstemmed = ["Antagonistic","Antagonises", "Antagonise", "Antagonizes", "inhibits", "inhibiting", "Inhibition", "inhibitory",\
	"outcompeted","lethal", "sublethal", "KILLING","kills","predator","anticorrelated","lysed", "lyses", "competing", "competition",\
	 "competed", "suppressed", "decrease", "lowered", "bacteriocin", "reduced", "bacteriocin", "bacteriocins", "against", "reduced",\
	 "antibacterial", "viability"]
stemmer = nltk.stem.snowball.EnglishStemmer()
negTerm = [stemmer.stem(i) for i in unstemmed]
negTerm = set(negTerm)

"""
Distance Cutoff for two terms
"""
cutoff = 10


"""
getNames:
	Given a file of abstracts, acquires the two terms to be searched from the file name

	file name is as follows:
		OBJECT_A#OBJECT_B
"""
def getNames(file):	
	def shorten(tup):
		return tup[0][0] + '. ' + tup[1]
	file = os.path.basename(file)
	name = os.path.splitext(file)[0]
	
	print(name)
	name = [i.split('_') for i in name.split('#')]
	#check if genus only
	
	print(name)
	if len(name[0]) ==1:
			return [[i[0]] for i in name]

	return [[" ".join(i), shorten(i), i[0]] for i in name] 

		#([" ".join(name[0]), shorten(name[0]), name[0][0]] , [" ".join(name[1]), shorten(name[1])])

"""
load: 
	Takes in an file containing abstracts and titles on separate lines
"""
def load(filename):
	with open(filename) as f:
		holder = []
		for i in f:
			#trim the 6 letter initalizer
			holder.append(i.strip().lower()[6:])
		return[(holder[i], holder[i+1]) for i in range(0, len(holder), 2)]



###TESTER
#returns a list of papers
#compirised of [TI, AB]
#where TI is list of str (sentence)
#and AB a list of sentences
#whcih are a list of strings
#[PAPER, PAPER] -> [TI, ABS] -> [SENT SENT] -> [WORD, WORD]

"""
stemFile:
	applies the snowball stemmer to a list of papers, stemming both abstracts and titles
"""
def stemFile(paperLst, spSet = {}):
	papers = []
	for paper in paperLst:
		try:
			papers.append((st.preprocess(paper[0], spSet), (st.preprocess(paper[1], spSet))))
		except:
			print(paper)
			raise

	stemmed = []
	for paper in papers:
		#title ,abs
		stemmed.append([[stemmer.stem(i) for i in paper[0][0]], [[stemmer.stem(word) for word in sentence] for sentence in paper[1]]\
			])
	#print("Preproc:", preproc[0][0][0])
	# untagged = [[[[tup[0] for tup in sentence] for sentence in component] for component in paper] for paper in preproc]
	# stemmed = [[[[stemmer.stem(word) for word in sentence] for sentence in component] for component in paper] for paper in untagged]
	return stemmed

# Check if a term from all three required categories is in the sentence
def sheck(sentence, spSet1, spSet2):
	b1,b2, neg= 0,0,0
	for word in sentence:

		if word in spSet1:
			b1 = 1
		elif word in spSet2:
			b2 = 1
		elif word in negTerm:
			neg = 1
	if b1 and b2 and neg:
		return True
	return False

#check if any sentences in teh abstract fit the term
def abcheck(abstract, spSet1, spSet2):
	b1, b2, d1, d2 = 0,0,0,0
	#DB raisees sensitivity but drastically drops specifiicity
	#Try forcing farness [] gap >3 tokens 
	db = 0
	for sentence in abstract:
		if 	sheck(sentence, spSet1, spSet2):
			return True


	return False



# def check(paper):
def execute(target):
	def write(enumPair, names):
		tnames = [i[0] for i in names]
		path = outdir + '#'.join(tnames) + '/' 
		if not os.path.exists(path):
			os.mkdir(path)
		#print(path +  str(enumPair[0])+".out")
		#print('___________--')
		with open(path + str(enumPair[0])+".out", 'w') as f:
			f.write(enumPair[1][0] + "\n")
			temp = st.sentSplit(enumPair[1][1])

			[f.write(i + "\n") for i in temp]


	papers = load(target)
	orig = [i for i in papers]

	#set up sets of bacterial species
	names = getNames(target)
	print(names)
	spSet1 = set(names[0])
	spSet2 = set(names[1])
	spSet = spSet1.union(spSet2)
	#Load all papers 
	allP = load(target)
	#stem all papers
	stemmed = stemFile(allP, spSet)
	output = open(outdir + "abcheck.out", "w")
	holder = []
	for original, paper in zip(enumerate(orig), stemmed):
		
		#Title fufills criteria
		if sheck(paper[0], spSet1, spSet2):
			holder.append("T")
			write(original, names)
			continue

		#Abstract fufills criteria
		if abcheck(paper[1], spSet1, spSet2):
			holder.append("T")
			write(original, names)
		else:
			holder.append("F")
		#print(len(holder), " | ", original[0])


	return holder




if __name__ == "__main__":
	
	# # #########DEBUG
	# target = "input/lactobacillus_acidophilus#escherichia_coli.compiled"
	# #set up sets of bacterial species
	# names = getNames(target)
	# print(names)
	# spSet1 = set(names[0])
	# spSet2 = set(names[1])
	# spSet = spSet1.union(spSet2)
	# #Load all papers 
	# allP = load(target)
	# #stem all papers
	# stemmed = stemFile(allP, spSet)
	# print('DEEEBUUUUGGG------------')
	# paper1 = stemmed[35]
	# print(paper1)
	# print(abcheck(paper1[1], spSet1, spSet2))-
	# raise	
	# ##########END
	

	target = "input/lactobacillus_acidophilus#escherichia_coli.compiled"
	#*target = "input/Actinomyces#Bacteroides.compiled"
	holder =execute(target)
	print(holder.count("T"))

	#EVALUTATION	
	annPath = "annotated/lactobacillus_acidophilus#escherichia_coli.ann"
	print("WITHOUT AMBIGUOUS/TITLE ONLY")
	evaluate.evaluate(holder, annPath, 1,  "testlog")
	print("WITH AMBIGUOUS/TITLE ONLY")
	evaluate.evaluate(holder, annPath, 0,  "testlog")
