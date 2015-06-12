#!usr/bin/env python3
from scipy.misc import comb
import scipy.stats as stats

#/////////////
# USER SET VARIABLES
#?////////////

# TARGET FILE
targetName = "2015-06-04-13_52.out"
target = "input/" + targetName
output = "output/hyprob" + targetName

holder = []

with open(target) as f:
	for i in f:
		#settle comments
		if i[0] == "#":
			continue
		else:
			holder.append(i.strip().split('\t'))


print(holder[0:4])
#generate total population
splat = [holder[i*6:i*6+6] for i in range(len(holder)//6)]

#save the named tuples for later use
named = splat

splat = [[i[-1]  for i in j ]for j in splat]


# #total number of papers: |T1| + |T2| - |T1 ^ T2|
# print(splat)
#total number of papers with negterm: |T1 ^ T3| + |T2 ^ T3| - |T1 ^ T2 ^ T3|
population = 0
#total number of papers with BOTH term && negterm: |T1 ^ T2 ^ T3|
tPopulation = 0

#Notes: UNDERREPRESENTS POPULATION SIZE
#		MAY OVERREPRESENT HITS
#		Reason: does not account for the third term in set addition
checked = set()
for i in named:
	# A + B i A ^ B
	#print(i)
	tup = [j[-1] for j in i]
	if i[0][0] not in checked and i[0][1] not in checked:
		population -= int(tup[4]) + int(tup[5]) - int(tup[3])
		checked.add(i[0][0])		
		checked.add(i[0][1])		
	#SP 1
	elif i[0][0] not in checked:
		population += int(tup[4]) - int(tup[3])
		checked.add(i[0][0])		
	#SP2
	elif i[0][1] not in checked:
		population += int(tup[5]) - int(tup[3])
		checked.add(i[0][1])

	tPopulation += int(tup[3])

cutoff = 0.01
#bone is the boneferroni
def hyprob(tup, bone = 4000):

	#count of sample values
	sample = int(tup[5]) + int(tup[4]) - int(tup[3])
	#count of 
	tSample = int(tup[3]) 
	print (sample, tSample)
	print(population, tPopulation)
	res = stats.hypergeom.pmf(tSample, population, tPopulation, sample)
	print(res)
	#quick hack to grab negative relationships only
	if sample > 0 and tSample/sample < 0.001:
		return 10
	return res*bone




with open (output, 'w') as f:
	for i, j in zip(splat, named):
		print("ANALYZE: ", j[0][0], j[0][1])
		prob = hyprob(i)
		if prob < cutoff:
			f.write("\t".join([j[0][0], j[0][1], str(prob)]) + '\n')




