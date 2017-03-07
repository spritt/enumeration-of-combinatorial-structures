import sys
from rules import *

# compute the valuations of a list of rules
# implementation of algorithm on page 28, section 1.4
def computeRuleValuations(rules):
    val = {}
    for r in rules:
        if isinstance(r.Value, Theta):
            continue
        rv = r.Value
        if isinstance(r, Atom):
            val[rv] = r.Size
        elif isinstance(r, Set) or (isinstance(r, KSet) and r.Rel == "<="):
            val[rv] = 0 # valuation of a set is 0
        elif rv not in val:
            val[rv] = sys.maxint
    return valuate(val, rules)

# current method is to sort by decreasing valuation
# and sort all Atom rules to the front of the list
def sortRulesByValuation(rules):
    vals = computeRuleValuations(rules)
    d = vals.items()
    print d
    d_sorted = sorted(d, key=lambda x:x[1], reverse=True)
    r_sorted = []
    for (k,v) in d_sorted:
        for r in rules:
            if r.Value == k or (isinstance(r.Value, Theta) and r.Value.SubRule == k):
                if isinstance(r, Atom) or isinstance(r, Set) or isinstance(r, KSet):
                    r_sorted = [r] + r_sorted
                else:
                    r_sorted.append(r)
    return r_sorted, vals
    
# helper for computeRuleValuations()
def valuate(v, rules):
    done = True
    for r in rules:
        if isinstance(r.Value, Theta):
            continue
        rv = r.Value
        prev = v[rv]
        if isinstance(r, Atom):
            continue
        elif isinstance(r, Set):
            continue
        elif isinstance(r, KSet):
            if rv.Rel == "<=":
                continue
            elif v[r.SubRule] < sys.maxint:
                    v[rv] = rv.Card * v[rv.SubRule]
        elif isinstance(r, Union):
            s1 = r.SubRule1 if not isinstance(r.SubRule1, Theta) else r.SubRule1.SubRule
            s2 = r.SubRule2 if not isinstance(r.SubRule2, Theta) else r.SubRule2.SubRule
            v[rv] = min(v[s1], v[s2])
        elif isinstance(r, Product):
            s1 = r.SubRule1 if not isinstance(r.SubRule1, Theta) else r.SubRule1.SubRule
            s2 = r.SubRule2 if not isinstance(r.SubRule2, Theta) else r.SubRule2.SubRule
            if v[s1] != sys.maxint and v[s2] != sys.maxint:
                v[rv] = v[s1] + v[s2]
        elif isinstance(r, Theta):
            v[rv] = v[r.SubRule]
        elif isinstance(r, Delta):
            v[rv] = v[r.SubRule]
        else: raise Exception('Unsupported rule')
        if v[rv] != prev: done = False
    if done: return v
    else: return valuate(v, rules)