from numpy import array, subtract
from numpy.linalg import norm
import sys
import gzip
import copy


def pagerank():
    inlinks = {}
    outlinks = {}
    with gzip.open(inputFile, 'rt') as f:
        for line in f:
            l = line.strip().split('\t')
            source_page = l[0]
            target_page = l[1]

            if not target_page in inlinks:
                inlinks[target_page] = [source_page]
            else:
                inlinks[target_page].append(source_page)
            if not source_page in inlinks:
                inlinks[source_page] = []
            if not source_page in outlinks:
                outlinks[source_page] = [target_page]
            else:
                outlinks[source_page].append(target_page)
            if not target_page in outlinks:
                outlinks[target_page] = []
    f.close()

    ################################################################################################
    # Finding the pagerank

    num_pages = len(outlinks)
    I = {}
    R = {}
    for key in outlinks:
        I[key] = 1 / num_pages

    def helper():
        for key in outlinks:
            R[key] = lambda_val / num_pages
        d = 0
        for p in outlinks:
            Q = []
            for q in outlinks[p]:
                if q in outlinks:
                    Q.append(q)
            if (len(Q) > 0):
                for q in Q:
                    R[q] += (1 - lambda_val) * I[p] / len(Q)
            else:
                d += (1 - lambda_val) * I[p] / num_pages
        for p in outlinks:
            R[p] += d            
    helper()
    while not converged(R, I):
        I = copy.deepcopy(R)
        helper()
        
        
    f1 = open(inLinksFile, "w")
    f2 = open(pagerankFile, "w")
    sorted_inlinks = dict(
        sorted(inlinks.items(), key=lambda x: len(x[1]), reverse=True))
    sorted_pagerank = dict(sorted(R.items(), key=lambda x: x[1], reverse=True))
    res1 = ""
    res2 = ""
    keys1 = list(sorted_inlinks.keys())
    keys2 = list(sorted_pagerank.keys())
    for i in range(0, min(k, num_pages)):
        key1 = keys1[i]
        key2 = keys2[i]
        res1 += str(key1) + "\t" + str(i + 1) + "\t" + \
            str(len(sorted_inlinks[key1])) + "\n"
        res2 += str(key2) + "\t" + str(i + 1) + "\t" + \
            str(sorted_pagerank[key2]) + "\n"
    f1.write(res1)
    f2.write(res2)
    f1.close()
    f2.close()


def converged(R, I):
    vector_R = array(list(R.values()))
    vector_I = array(list(I.values()))
    vector = subtract(vector_I, vector_R)
    return abs(norm(vector)) < tau


if __name__ == '__main__':
    # Read arguments from command line; or use sane defaults for IDE.

    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "links.srt.gz"
    lambda_val = float(sys.argv[2]) if argv_len >= 3 else 0.2
    tau = float(sys.argv[3]) if argv_len >= 4 else 0.005
    inLinksFile = sys.argv[4] if argv_len >= 5 else "inlinks.txt"
    pagerankFile = sys.argv[5] if argv_len >= 6 else "pagerank.txt"
    k = int(sys.argv[6]) if argv_len >= 7 else 100
    pagerank()
    ...
