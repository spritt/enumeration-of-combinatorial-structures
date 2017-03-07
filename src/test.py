from rules import *
from convert import *
from valuate import *
from generate import *

# enumerate an object from standard form
def StandardForm(rules, n, sym, norm):
    sortedRules, v = sortRulesByValuation(rules)
    tab = EnumerateFromStandardForm(sortedRules, n, v)
    seq = []
    fac = 1
    for i in range(n):
        if norm: fac *= i if i > 0 else 1 # norm = True for labelled classes
        seq += [int(tab[i][sym] * fac)]
    return seq

# some test cases
eq1 = Union('X', Atom(1), Product('X', 'X'))
eq2 = Union('X', Atom(1), Union(Product(Atom(1), 'X'), Product(Product(Atom(1), 'X'), 'X')))
eq3 = Product('X', Atom(1), Set('X'))
eq4 = Set('X', Atom(1))
eq5 = Sequence('X', Atom(1))
eq6 = Sequence('X', Union(Atom(1), Atom(2)))
eq7 = Product('X', Atom(1), Sequence('X'))
eq8 = Cycle('X', Atom(1))
eq9 = Cycle('X', Atom(2))

# constrained sets - currently under construction
eq10 = Union('X', Atom(1), KSet('X', "=", 2))
eq11 = Union('X', Atom(1), KSet('X', "<=", 2))

eqs = [eq3]

# run the tests

def run(eq, eqs):
    for eq in eqs:
    	rules = ConvertToStandardForm(eq)
    	for r in rules:
    	    print r
    	print StandardForm(rules, 10, 'X', True)

# test unlabelled rooted trees: H = Z * Set(H)
r = [Atom('A', 1), Product('H', 'A', 'B'), Theta('D', 'H'), Delta('C', 'D'), Product(Theta('B'), 'B', 'C'), Set('B', 'H')]
v = computeRuleValuations(r)
#v = {'H': 1, 'A': 1, 'B': 0, 'C': 1, 'D': 1}
tab = EnumerateFromStandardForm(r, 10, v)
for i in range(10):
    print tab[i]['H']
