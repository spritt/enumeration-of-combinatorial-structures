import sys
from rules import *

# compute the valuations of a list of rules
# implementation of algorithm on page 28, section 1.4
def computeRuleValuations(rules):
    val = {}
    for r in rules:
        rv = r.Value if len(r.Value) == 1 else r.Value[1]
        if isinstance(r, Atom):
            val[rv] = r.Size
        elif isinstance(r, Set):
            val[rv] = 0 # valuation of a set is 0
        elif rv not in val:
            val[rv] = sys.maxint
    return valuate(val, rules)

# current method is to sort by decreasing valuation
# and sort all Atom rules to the front of the list
def sortRulesByValuation(rules):
    vals = computeRuleValuations(rules)
    d = vals.items()
    #print d
    d_sorted = sorted(d, key=lambda x:x[1], reverse=True)
    r_sorted = []
    for (k,v) in d_sorted:
        for r in rules:
            if r.Value == k or (len(r.Value) == 2 and r.Value[1] == k):
                if isinstance(r, Atom) or isinstance(r, Set) or isinstance(r, KSet):
                    r_sorted = [r] + r_sorted
                else:
                    r_sorted.append(r)
    return r_sorted, vals
    
# helper for computeRuleValuations()
def valuate(v, rules):
    done = True
    for r in rules:
        rv = r.Value if len(r.Value) == 1 else r.Value[1]
        prev = v[rv]
        if isinstance(r, Atom):
            continue
        elif isinstance(r, Set) or isinstance(r, KSet):
            continue
        elif rv in v and v[rv] == 0:
            continue
        elif isinstance(r, Union):
            l = r.SubRule1 if len(r.SubRule1) == 1 else r.SubRule1[1]
            r = r.SubRule2 if len(r.SubRule2) == 1 else r.SubRule2[1]
            v[rv] = min(v[l], v[r])
        elif isinstance(r, Product):
            l = r.SubRule1 if len(r.SubRule1) == 1 else r.SubRule1[1]
            r = r.SubRule2 if len(r.SubRule2) == 1 else r.SubRule2[1]
            v[rv] = v[l] + v[r]
        else: raise Exception('Unsupported rule')
        if v[rv] != prev or v[rv] > sys.maxint / 2: done = False
    if done: return v
    else: return valuate(v, rules)