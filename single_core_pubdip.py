#!/usr/bin/env python3

"""
pubdip.py: 
   Takes in a tsv consisting of multiple lines of TSV'd terms. Joins them with 'AND' and uses as the base query

    The base query, along with a negTerm variant, is then submitted to the entrez database.

    A tsv containing the Query targets and the resultant count values is returned
"""


from Bio import Entrez, Medline
from time import strftime
import os
import modfile


termDict = dict()

"""
pubmedCount:
    takes in three terms, checks for number of papers for:
        term1 AND term2
        term1
        term2
        term1 AND term2 AND term3
        term1 AND term3
        term2 AND term3
        
    returns the above terms asa  list of 6-tuples
"""
def pubmedCount(term1, term2, term3, retry = 0, debug = 0):
    def getCount(query):
        if query in termDict:
            print("repeated")
            return termDict[query]
        handle = Entrez.esearch(db = "pubmed", term = query)
        record = Entrez.read(handle)
        count = record["Count"]
        
        if debug:
            print("GETCOUNT query: ", query)
            print("COUNT = ", count)
        
        termDict[query] = count
        return count

    Entrez.email = "kmklim@gis.a-star.edu.sg"

    baseQuery = ' '.join([term1, "AND", term2])
    if debug:
        print("Searching: ", baseQuery)

    #raw queries
    queries = [baseQuery, term1, term2]
    #negTerm queries
    nQuery = [' AND '.join([i, term3]) for i in queries]
    queries += nQuery
    
    lTerms = [[term1, term2], [term1, ' '], [term2, ' ']] * 2
    try:
        result = [i + [getCount(j)] for i,j in zip(lTerms, queries)]
    except:
        if retry <3:
            return pubmedCount(term1, term2, term3, retry + 1, debug)
        else:
            print("ERROR: UNABLE TO QUERY ", term1, " | ", term2, )
    
    print("RESULT:", result)
    with open(rawOut, 'a') as f:
        for i in result:
            f.write("\t".join(i) + '\n')
    with open(twoOut, 'a') as f:
        f.write("\t".join(result[0]) + '\n')
    return

"""
readfile:
    takes in a tsv of line separated species pairs

    returns a list of [sp1, sp2] pairs

    if genus is specified, returns a list of [g1, g2] pairs

    if genus is not specified, can be used for any paired data
"""

def readFile(fileName):
    lst = []        
    with open(fileName) as f:
        for i in f:
            lst.append(i.strip().split('\t'))

    return lst

"""
execute:
    execution script for the whole package
    takes in a list containing ALL combinations of [T1, T2, T3] wanted for pubmedCount and the number of cores to use

    returns 
"""

if __name__ == "__main__":
    import argparse

    #/////////////#
    #  ARGUMENTS  #
    #/////////////#

    parser = argparse.ArgumentParser()
    parser.add_argument( "target", help ="Target file. File must be a line-separated list of tab separated term pairs. eg: Escherichia coli  Pseudomonas aeruginosa")
    parser.add_argument( "-o", "--outdir", help ="Specify output directory name within output/")
    args = parser.parse_args()

    target = args.target
    

    #/////////////////#
    #  INITIAL SETUP  #
    #/////////////////#

    """
    Negative terms
        These are the query terms (term3) submitted along side the species
    """
    negTerm = "(inhibit | inhibits | inhibition | inhibited) "
    negTerm = ("(Antagon*|" 
            "outcompet*| lethal| sublethal| kill*| predat*| anticorrelated| lyse*| compet*|"
            "suppress*|  bacteriocin*|"
            "antibacterial | viab*)")

    outDir = "output/"
    if args.outdir:
        outDir = outDir + args.outdir + '/'


    fileName = modfile.FileName(target)
    baseName = fileName.modbase(strftime("%Y-%m-%d-%H_%M") + '_')
    
    rawOut = outDir + baseName
    twoOut = outDir + "twocount_" + baseName
    print("-----Output Names------")
    print("BASENAME: ", baseName)
    print(rawOut)
    print(twoOut)
    print("-----Output Names------")

    if not os.path.exists("output"):
        os.makedirs("output")
    if args.outdir:
        if not os.path.exists("output/" + args.outdir):
            os.makedirs("output/" + args.outdir)



    #check if file blurb has already been written
    if not os.path.isfile(rawOut):
        with open(rawOut, 'w') as f:
            f.write("#negTerm: " + negTerm + '\n'
                    "#row1-3: raw query | both species, species 1, species 2\n"
                    "#row4-6: with negTerm | both species, species 1, species 2\n"
                    "#Target File:" + target + "\n"
                )
    if not os.path.isfile(twoOut):
        with open(twoOut, 'w') as f:
            f.write("#negTerm: " + negTerm + '\n'
                    "#row1-3: raw query | both species, species 1, species 2\n"
                    "#row4-6: with negTerm | both species, species 1, species 2\n"
                    "#Target File:" + target + "\n"
                )


    #/////////////////////
    #  END INITIAL SETUP
    #/////////////////////

    lst = readFile(target)

    for i in lst:
        pubmedCount(i[0], i[1], negTerm)
