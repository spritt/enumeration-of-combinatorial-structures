from rules import *
from convert import *
from valuate import *
from generate import *

def StandardForm(rules, n, sym, norm):
    sortedRules, v = sortRulesByValuation(rules)
    tab = EnumerateFromStandardForm(sortedRules, n, v)
    seq = []
    fac = 1
    for i in range(n):
        if norm: fac *= i if i > 0 else 1
        seq += [int(tab[i][sym] * fac)]
    return seq

eq1 = Union('X', Atom(1), Product('X', 'X'))
eq2 = Union('X', Atom(1), Union(Product(Atom(1), 'X'), Product(Product(Atom(1), 'X'), 'X')))
eq3 = Product('X', Atom(1), Set('X'))
eq4 = Set('X', Atom(1))
eq5 = Sequence('X', Atom(1))
eq6 = Sequence('X', Union(Atom(1), Atom(2)))
eq7 = Product('X', Atom(1), Sequence('X'))
eq8 = Cycle('X', Atom(1))
eq9 = Cycle('X', Atom(2))
#eq10 = Union('X', Atom(1), KSet('X', "=", 2))
#eq11 = Union('X', Atom(1), KSet('X', ">=", 2))

eqs = [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9]

eq = eq9

rules = ConvertToStandardForm(eq)
for r in rules:
    print r
print StandardForm(rules, 10, 'X', True)