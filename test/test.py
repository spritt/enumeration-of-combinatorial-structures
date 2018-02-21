from core.rules import *
from core.convert import *
from core.valuate import *
from core.generate import *

# enumerate an object from standard form
def StandardForm(rules, n, sym, norm):
    v = computeRuleValuations(rules)
    print v
    tab = EnumerateFromStandardForm(rules, n, v)
    seq = []
    fac = 1
    for i in range(n+1):
        if norm: fac *= i if i > 0 else 1 # norm = True for labelled classes
        seq += [tab[i][sym] * fac]
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
eq10 = Union('X', Atom(1), Union(Atom(1), Product(Atom(1), KSet('X', "=", 3))))
eq11 = Union('X', Atom(1), KSet('X', "<=", 2))
eq12 = Union('X', Atom(1), KSet('X', "=", 3))
eq13 = Union('X', Atom(1), KSet('X', ">=", 3))

eq14 = KSet('X', Atom(1), ">=", 2)
eq15 = KCycle('X', Atom(1), "=", 2)

eq16 = Set('X', Atom(1))

eq17 = KSequence('X', Atom(1), "=", 4)
eq18 = KSequence('X', Atom(1), ">=", 4)
eq19 = KSequence('X', Atom(1), "<=", 4)

eq20 = Union('X', Atom(1), KCycle('X', "=", 2))
eq21 = Union('X', Atom(1), KCycle('X', "=", 3))
eq22 = KCycle('X', Atom(1), "<=", 4)
eq23 = KCycle('X', Union(Atom(1), Atom(1)), "<=", 3)

eq24 = KSequence('X', Union(Atom(1), Atom(1)), "<=", 3)

eq25a = Set('X', 'Y')
eq25b = KCycle('Y', Atom(1), "<=", 3)

#eqs = [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11, eq12, eq13]
#eqs = [eq12, eq13]
#eqs = [eq15]
#eqs = [eq17, eq18, eq19]
#eqs = [eq20, eq21, eq22, eq23]
#eqs = [eq24]
eqs = [eq25a, eq25b]

# run the tests

def run(eqs, labeled=True):
    i = 0
    for eq in eqs:
        i += 1
        print("--------------------------------------- " +
            "Test " + str(i) + " of " + str(len(eqs)) + 
            " ---------------------------------------")
    	rules = ConvertToStandardForm([eq], labeled)
    	#for r in rules:
    	#    print r
    	print StandardForm(rules, 10, 'X', labeled)
    print("Done")
    print("")

run(eqs, False)

'''
#eq14 = Set('X', Cycle(Atom(1)))

eq = Product('H', Atom(1), Set('H'))
rules1 = ConvertToStandardForm([eq], labeled=False)
print StandardForm(rules1, 10, 'H', False)

print("")

eq8 = Cycle('X', Atom(1))

rules2 = ConvertToStandardForm([eq8], labeled=True) 
print StandardForm(rules2, 10, 'X', True)

eq8 = Cycle('X', Atom(1))

print("")

rules3 = ConvertToStandardForm([eq8], labeled=False) 
print StandardForm(rules3, 10, 'X', False)

print("")

eq1 = Cycle('X', Atom(1))
eq2 = Set('Y', 'X')

rules4 = ConvertToStandardForm([eq1, eq2], labeled=False)
print StandardForm(rules4, 10, 'Y', False)

print("")

eq1 = Product('U', Atom(1), Set('U'))
eq2 = Cycle('V', 'U')
eq3 = Set('W', 'V')

rules5 = ConvertToStandardForm([eq1, eq2, eq3], labeled=False)
print StandardForm(rules5, 10, 'W', False)

print("")

eq1 = KSet('X', Atom(1), ">=", 1)
eq2 = Sequence('Y', 'X')

rules6 = ConvertToStandardForm([eq1, eq2], labeled=True)
print StandardForm(rules6, 10, 'Y', True)

print("")
print("")
print("")

eq = Atom(1)
r, _, s = exp({}, 66, 'X', 1)
for k,v in r.iteritems():
    print v
print s

print("")

eq = KSequence('X', Atom(1), "=", 4)
r, _ = convertKSequence(eq, {}, 65, True)
for k,v in r.iteritems():
    print str(k) + " -> " + str(v)

print("")

eq = KCycle('X', Atom(1), "=", 5)
rules = ConvertToStandardForm([eq], labeled=True)
print StandardForm(rules, 10, 'X', True)

print("")
print("")
print("")

eq = Union('P', Atom(1), KSet('P', "<=", 2))
rules = ConvertToStandardForm([eq], labeled=False)
print StandardForm(rules, 10, 'P', False)

print("")

eq1 = KSet('X', 'Y', "<=", 4)
eq2 = Cycle('Y', Atom(1))
rules = ConvertToStandardForm([eq1, eq2], labeled=False)
print StandardForm(rules, 10, 'X', False)
'''

# test unlabeled rooted trees: H = Z * Set(H)
#r = {'A': Atom('A', 1), 'H': Product('H', 'A', 'B'), 'D': Theta('D', 'H'), 'C': Delta('C', 'D'), 
#        Theta('B'): Product(Theta('B'), 'B', 'C'), 'B': Set('B', 'H')}
#print StandardForm(r, 10, 'H', False)

# test labeled hierarchies: H = Z + Set(H, card >= 2)
#r = {'A': Atom('A', 1), 'H': Union('H', 'A', 'U'), Theta('U'): Product(Theta('U'), 'X', 'V'), Theta('V'): Product(Theta('V'), 'X', 'W'), 
#    Theta('W'): Product(Theta('W'), 'X', 'W'), 'X': Theta('X', 'H'), 'U': KSet('U', 'H', ">=", 2), 'V': KSet('V', 'H', ">=", 1), 'W': Set('W', 'H')}
#print StandardForm(r, 10, 'H', True)
