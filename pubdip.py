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

from urllib.error import HTTPError
import multiprocessing

"""
pubmedCount:
    takes in three terms, checks for number of papers for:
        term1 AND term2
        term1
        term2
        term1 AND term2 AND term3
        term1 AND term3
        term2 AND term3
        
    returns a list of 6tuples
"""
def pubmedCount(term1, term2, term3, retry = 0, debug = 0):
    def getCount(query):
        handle = Entrez.esearch(db = "pubmed", term = query)
        record = Entrez.read(handle)
        count = record["Count"]
        if debug:
            print("GETCOUNT query: ", query)
            print("COUNT = ", count)
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
    return result

"""
readfile:
    takes in a tsv of line separated species pairs

    returns a list of [sp1, sp2] pairs

    if genus is specified, returns a list of [g1, g2] pairs

    if genus is not specified, can be used for any paired data
"""

def readFile(fileName, genus = 0):
    lst = []
    glst = set()
        
    with open(fileName) as f:
        for i in f:
            if genus:
                temp = i.strip().split('\t')
                temp = (temp[0].strip().split(' ')[0], temp[1].strip().split(' ')[0])
                if temp[::-1] in glst:
                    continue
                glst.add(temp)

            else:
                lst.append(i.strip().split('\t') + [negTerm])
    if genus:
        return list(glst)
    return lst

def execute(terms, cores):
    with multiprocessing.Pool(cores) as pool:
            mappedRuns = pool.starmap(pubmedCount, terms) 
    return mappedRuns



if __name__ == "__main__":
    import argparse

    #/////////////#
    #  ARGUMENTS  #
    #/////////////#

    parser = argparse.ArgumentParser()
    parser.add_argument( "target", help ="Target file. File must be a line-separated list of tab separated term pairs. eg: Escherichia coli  Pseudomonas aeruginosa")
    parser.add_argument("-g", "--genus", action = "store_true", default = False, help = "Flag for Genus only search")
    parser.add_argument("-d", "--debug", action = "store_true", default = False, help = "Enable debug mode")
    # ##EXPERIMENTAL
    # parser.add_argument("-p", "--pair", action = "store_true", default = False, help = "Search only for pair counts")
    # parser.add_argument("-s", "--sum", action = "store_true", default = False, help = "return only counts")
    parser.add_argument("-c", "--cores", default = 10, type = int, help = "number of cores")
    args = parser.parse_args()

    target = args.target
    cores = args.cores

    print("-------Testing Parameters---------")
    print("Genus level search: " ,args.genus)
    print("Debug mode: " ,args.debug)
    print("corecount", str(cores))
    print("-------Testing Parameters---------")
    

    #/////////////////#
    #  INITIAL SETUP  #
    #/////////////////#

    """
    Negative terms
        These are the query terms (term3) submitted along side the species
    """
    #negTerm = "(inhibit | inhibits | inhibition | inhibited) "
    negTerm = "(Antagonistic| Antagonises| Antagonise| Antagonizes| inhibits| inhibiting| Inhibition| inhibitory| \
        outcompeted| lethal| sublethal| KILLING| kills| predator| anticorrelated| lysed| lyses| competing| competition| \
         competed| suppressed|  bacteriocin|  bacteriocin| bacteriocins|  \
         antibacterial | viability)"

    outDir = "output/"
    baseName = strftime("%Y-%m-%d-%H_%M") + ".out"
    rawOut = outDir + baseName
    twoOut = outDir + "twocount_" +baseName
    sumOut = outDir + "sum_" + baseName
    print("-----Output Names------")
    print(rawOut)
    print(twoOut)
    print(sumOut)
    if not os.path.exists("output"):
        os.makedirs("output")

    #/////////////////////
    #  END INITIAL SETUP
    #/////////////////////

    lst = readFile(target, args.genus)

    print([i[:2] for i in lst])
    mappedRuns = execute(lst, cores)

    #///////////////#
    #  FILE OUTPUT  #
    #///////////////#


    with open(rawOut, 'w') as f:
        f.write("#negTerm: (Antagonistic| Antagonises| Antagonise| Antagonizes| inhibits| inhibiting| Inhibition| inhibitory|     outcompeted| lethal| sublethal| KILLING| kills| predator| anticorrelated| lysed| lyses| competing| competition|      competed| suppressed|  bacteriocin|  bacteriocin| bacteriocins|       antibacterial | viability)\n"
                "#row1-3: raw query | both species, species 1, species 2\n"
                "#row4-6: with negTerm | both species, species 1, species 2\n"
            )
        for i in mappedRuns:
            for j in i:
                f.write("\t".join(j) + '\n')

    paperSum = 0

    with open(twoOut, 'w') as f:
        for i in mappedRuns:
            paperSum += int(i[0][-1])
            f.write("\t".join(i[0]) + '\n')

    with open(sumOut, 'w') as f:
        f.write(str(paperSum))
