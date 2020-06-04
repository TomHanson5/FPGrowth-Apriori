"""CSC 240: Frequent Itemset Mining With Apriori.

Code based on psudocode from Data Mining Concepts and Techniques by Han, et. al
All function titles are either descriptive or match those from the book.

Some key functions (scanning, data loading, etc) have some runtime monitors.
By uncommenting the line at the start ('start = time.time()'), the end,
and the print statement,
the runtime in seconds will be printed for that function call.

Thomas Hanson
"""

import itertools
import time
import math


def main(argv):
    start = time.time()
    data = data_load(argv[0])
    d = list(map(set, data))
    minSupCount = math.ceil(argv[1]*len(d))
    c1 = get_k1_itemsets(data, minSupCount)
    # Generate set of length 1 candidates
    L1 = count_scan(d, c1, minSupCount)
    l = [L1]  # List of Frequent Itemsets
    k = 2
    while (len(l[k-2]) > 0):  # Continue until empty
        ck = apriori_gen(l[k-2], k)
        lk = count_scan(d, ck, minSupCount)

        l.append(lk)
        k += 1

    l = makePrintable(l)
    print(l)
    end = time.time()
    print("total time: ", (end-start))


def apriori_gen(lk, k):
    """Generate k candidates from k-1 frequent itemset
    Returns candidates
    """
    # start = time.time()
    ret = [] # maybe make set
    length = len(lk)
    for i in range(length):
        for j in range(i+1, length):
            L1 = list(lk[i])[:k-2]
            L2 = list(lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                c = lk[i] | lk[j]
                if has_infrequent_subset(c, lk):
                    del c # prune step
                else:
                    ret.append(c)
    # end = time.time()
    # print('apriori: ', (end - start))
    return ret


def has_infrequent_subset(candidate, frequentSets):
    """Pruning function,
    takes frequent k-candidates and compares with k-1 frequent itemsets
    Returns boolean
    """
    for s in get_all_subsets(candidate):
        if not s.issubset(frequentSets):
            return False
        return True


# Helper Functions
def data_load(filename):
    """Load in data from file. Assumed to be comma separated value file
    such as the UCI Census Income Dataset
    (http://archive.ics.uci.edu/ml/datasets/Adult)

    Returns data as 2d list with all values seperated by a comma
    """
    # start = time.time()
    file = open(filename, 'r')
    transactions = file.readlines()
    file.close()
    for i in range(len(transactions)):
        line = transactions[i]
        line = line.strip().rstrip(',')
        line = line.split(',')
        transactions[i] = line

    # end = time.time()

    # print("data loading: ", (end - start))
    return transactions


def get_all_subsets(itemset):
    """Find and return all k-1 subsets
    """
    k = len(itemset)
    ret = [set(i) for i in itertools.combinations(itemset, k)]
    return ret


def get_k1_itemsets(data, minSup):
    """Find and Return frequent itemsets of length 1
    """
    # start = time.time()
    counts = dict()
    for trans in data:
        for item in trans:
            if item not in counts:
                counts[item] = 1
            else:
                counts[item] += 1
                

    for item, sup in list(counts.items()):
        if sup < minSup:
            del counts[item]
        
    # using a frozen set so that it is immutable
    # and can be made the key of a dictionary
    out = [frozenset({key, }) for key in counts.keys()]
    # end = time.time()
    # print("getting k=1: ", (end - start))
    return out


def count_scan(d, ck, minSupCount):
    """Mirrors lines 4 to 9 of psudocode from textbook, figure 6.4:
    The subloop of transforming Ck to Lk
    Takes d dataset, ck candidates, and minSupCount as an integer value

    need 4 speed

    returns Lk
    """
    # start = time.time()
    counts = dict()
    # Lines 4-8
    for transaction in d:
        for candidate in ck:
            if candidate.issubset(transaction):
                if candidate not in counts:
                    counts[candidate] = 1
                else:
                    counts[candidate] += 1

    Lk = []
    for key in counts:
        if counts[key] >= minSupCount:
            Lk.insert(0, key)

    # end = time.time()
    # print('scanning: ', (end - start))
    return Lk


def makePrintable(lk):
    """Transforms the final set of frequent itemsets to a set of strings
    Remove the 'frozenset{' and more from the final strings
    Make lk to the form: [['m'], ['o'], ... ['m', 'o'], ... ['o','k','e']]
    Based on the example from textbook problem 6.6

    Returns a new list in easilly readable form
    """
    ret = []
    for k in lk:
        for item in k:
            item = str(item)
            temp = item.split('\'')
            ret += [temp[1::2]]
    return ret


if __name__ == "__main__":
    args = ["Data.csv", .2]
    main(args)
