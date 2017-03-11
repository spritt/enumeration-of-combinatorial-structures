from rules import *
from convert import *
from valuate import *
from generate import *

# enumerate an object from standard form
def StandardForm(rules, n, sym, norm):
    v = computeRuleValuations(rules)
    tab = EnumerateFromStandardForm(rules, n, v)
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

def run(eqs):
    for eq in eqs:
    	rules = ConvertToStandardForm(eq)
    	for r in rules:
    	    print r
    	print StandardForm(rules, 10, 'X', True)

# test unlabeled rooted trees: H = Z * Set(H)
r = {'A': Atom('A', 1), 'H': Product('H', 'A', 'B'), 'D': Theta('D', 'H'), 'C': Delta('C', 'D'), 
        Theta('B'): Product(Theta('B'), 'B', 'C'), 'B': Set('B', 'H')}
print StandardForm(r, 10, 'H', False)

# test labeled hierarchies: H = Z + Set(H, card >= 2)
r = {'A': Atom('A', 1), 'H': Union('H', 'A', 'U'), Theta('U'): Product(Theta('U'), 'X', 'V'), Theta('V'): Product(Theta('V'), 'X', 'W'), 
    Theta('W'): Product(Theta('W'), 'X', 'W'), 'X': Theta('X', 'H'), 'U': KSet('U', 'H', ">=", 2), 'V': KSet('V', 'H', ">=", 1), 'W': Set('W', 'H')}
print StandardForm(r, 10, 'H', True)