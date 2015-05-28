#!/usr/bin/env python3

"""
pubdip.py:
    Takes in a tsv consisting of multiple lines of TSV'd terms. Joins them with 'AND' and uses as the base query

    The base query, along with a negTerm variant, is then submitted to the entrez database.

    A tsv containing the Query targets and the resultant count values is returned
"""


from Bio import Entrez, Medline

from time import strftime, sleep
import os
import sys
import argparse
from urllib.error import HTTPError
import multiprocessing
#import nltk.stem.snowball.EnglishStemmer as stemmer

parser = argparse.ArgumentParser()
parser.add_argument( "target", help ="Target file. File must be a line-separated list of tab separated term pairs. eg: Escherichia coli  Pseudomonas aeruginosa")
parser.add_argument("-g", "--genus", action = "store_true", default = False, help = "Flag for Genus only search")
parser.add_argument("-d", "--debug", action = "store_true", default = False, help = "Enable debug mode")
##EXPERIMENTAL
parser.add_argument("-p", "--pair", action = "store_true", default = False, help = "Search only for pair counts")
parser.add_argument("-s", "--sum", action = "store_true", default = False, help = "return only counts")
args = parser.parse_args()

target = args.target
print("-------Testing Parameters---------")
print("Genus level search: " ,args.genus)
print("Debug mode: " ,args.debug)
print("-------Testing Parameters---------")
####################
#USER SET VARIABLES#
####################
terms = ["TI", "AB"]
cores = 10

"""
Negative terms
    These are the query terms (term3) submitted along side the species
"""
#negTerm = "(inhibit | inhibits | inhibition | inhibited) "
negTerm = "(Antagonistic| Antagonises| Antagonise| Antagonizes| inhibits| inhibiting| Inhibition| inhibitory| \
    outcompeted| lethal| sublethal| KILLING| kills| predator| anticorrelated| lysed| lyses| competing| competition| \
     competed| suppressed|  bacteriocin|  bacteriocin| bacteriocins|  \
     antibacterial | viability)"



output = "output/" + strftime("%Y-%m-%d-%H_%M") + ".out"
if not os.path.exists("output"):
    os.makedirs("output")

with open(output, 'w') as f:
    f.write("#negTerm: " + negTerm + '\n')
    f.write('#row1-3: raw query | both species, species 1, species 2\n'
        '#row4-6: with negTerm | both species, species 1, species 2 \n')

if args.sum:
    paperSum = []

def preProc(data):
    return data.split('\n')

def pubmedSearch(term1, term2, term3, retry = 0):
    def getCount(query):
        handle = Entrez.esearch(db = "pubmed", term = query)
        record = Entrez.read(handle)
        count = record["Count"]
        if args.debug:
            print("GETCOUNT: ", query)
            print("COUNT = ", count)
        return count
        
    baseQuery = ' '.join([term1, "AND", term2])
    if args.debug:
        print("Searching: ", baseQuery)
    #raw queries
    queries = [baseQuery, term1, term2]

    #negTerm queries
    nQuery = [' AND '.join([i, term3]) for i in queries]
    queries += nQuery
    Entrez.email = "kmklim@gis.a-star.edu.sg"
    if args.debug:
        print("writing: ", baseQuery)
    if args.sum:

        try:
            queryCount = int(getCount(queries[0]))
        except:
            if retry <3:
                return pubmedSearch(term1, term2, term3, retry + 1)
            else:
                print("FAILED TO SEARCH: ", term1, " | ", term2)
        with open(output[:-4] + "_SUM_parts.out", 'a') as f:
            f.write("\t".join([term1, term2, str(queryCount)]) + '\n')
        return queryCount

    elif args.pair:
        with open(output, 'a') as f:
            f.write('\t'.join([term1, term2, getCount(queries[0]) + '\n']))
    else:

        with open(output, 'a') as f:
            # Without negative term
            f.write('\t'.join([term1, term2, getCount(queries[0]) + '\n']))
            f.write('\t'.join([term1, ' ', getCount(queries[1]) + '\n']))
            f.write('\t'.join([term2, ' ', getCount(queries[2]) + '\n']))
            # With negative term
            f.write('\t'.join([term1, term2, getCount(nQuery[0]) + '\n']))
            f.write('\t'.join([term1, ' ', getCount(nQuery[1]) + '\n']))
            f.write('\t'.join([term2, ' ', getCount(nQuery[2]) + '\n']))


    
lst = []
glst = set()
    
with open(target) as f:
    for i in f:
        if args.genus:
            temp = i.strip().split('\t')
            temp = (temp[0].strip().split(' ')[0], temp[1].strip().split(' ')[0])
            if temp[::-1] in glst:
                continue
            glst.add(temp)

        else:
            lst.append(i.strip().split('\t') + [negTerm])

    #print(lst)

pool = multiprocessing.Pool(cores)
if args.genus:
    mappedRuns = pool.starmap(pubmedSearch, list(glst))
else:
    mappedRuns = pool.starmap(pubmedSearch, lst)

if args.sum:
    total = sum(mappedRuns)
    print("SUM: ", total)
    with open(output[:-4] + "_SUM.out", 'w') as f:
        f.write(str(total))

if __name__ == "__main__":
    pass
