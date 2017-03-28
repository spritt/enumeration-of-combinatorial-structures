import sys
from rules import *

# compute the valuations of a list of rules
# implementation of algorithm on page 28, section 1.4
def computeRuleValuations(rules):
    val = {}
    for _, r in rules.iteritems():
        if isinstance(r.Value, Theta):
            continue
        if isinstance(r, Atom):
            val[r.Value] = r.Size
        elif isinstance(r, Set) or (isinstance(r, KSet) and r.Rel == "<="):
            val[r.Value] = 0 # valuation of a set is 0
        elif isinstance(r, Cycle):
            val[r.Value] = 1
        elif r.Value not in val:
            val[r.Value] = sys.maxint
    return valuate(val, rules)
    
# helper for computeRuleValuations()
def valuate(v, rules):
    done = True
    for _, r in rules.iteritems():
        if isinstance(r.Value, Theta):
            continue
        rv = r.Value
        prev = v[rv]
        if isinstance(r, Atom):
            continue
        elif isinstance(r, Set):
            continue
        elif isinstance(r, Cycle):
            continue
        elif isinstance(r, KSet):
            if r.Rel == "<=":
                continue
            elif v[r.SubRule] < sys.maxint:
                    v[rv] = r.Card * v[r.SubRule]
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
            if r.SubRule in v:
                v[rv] = v[r.SubRule]
        elif isinstance(r, Delta):
            if r.SubRule in v:
                v[rv] = v[r.SubRule]
        else: raise Exception('Unsupported rule')
        if v[rv] != prev: done = False
    if done: return v
    else: return valuate(v, rules)