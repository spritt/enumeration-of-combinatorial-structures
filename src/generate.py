from rules import *
from util import *

def EnumerateFromStandardForm(rules, n, v):
    t = {}
    for k in range(n+1):
        for r in rules:
            t = evaluateRule(r, rules, k, t, v)
    return t

def evaluateRule(r, rules, k, table, vals):
    # initialize
    if k not in table:
        table[k] = {}

    rule = rules[r]

    if isinstance(rule, Set) or (isinstance(rule, KSet) and rule.Rel == "<="):
        if k == 0: table[k][r] = 1.0
        return table

    if isinstance(rule, Cycle):
        return table

    # evaluate coefficient
    table[k][r] = evaluate(r, rules, k, table, vals, [r], [k])

    if isinstance(r, Theta) and r.SubRule not in table[k]:
        table[k][r.SubRule] = float(table[k][r]) / k if k > 0 else 0.0

    return table

# recursively evaluate a coefficient
def evaluate(r, rules, k, table, vals, r0, k0):
    def subEval(r1, k1):
        return 0.0 if r1 in r0 and k1 in k0 else evaluate(r1, rules, k1, table, vals, r0 + [r1], k0 + [k1])
    # base case
    if r in table[k]:
        return table[k][r]
    # 0 if k < valuation
    if isinstance(r, Theta) and k < vals[r.SubRule]:
        return 0.0
    elif not isinstance(r, Theta) and k < vals[r]:
        return 0.0
    # begin recursive evaluation
    rule = rules[r]
    # A = Z
    if isinstance(rule, Atom):
        return 1.0 if rule.Size == k else 0.0
    # A = B + C
    elif isinstance(rule, Union):
        return subEval(rule.SubRule1, k) + subEval(rule.SubRule2, k)
    # A = B * C
    elif isinstance(rule, Product):
        conv = 0.0
        for i in range(0,k+1):
            a, b = subEval(rule.SubRule1, i), subEval(rule.SubRule2, k-i)
            conv += a * b if a != 0.0 and b != 0.0 else 0.0
        return conv
    elif isinstance(rule, Set) or (isinstance(rule, KSet) and rule.Rel == "<="):
        return 1.0
    elif isinstance(rule, Cycle):
        return subEval(Theta(r), k) / k if k > 0 else 0.0
    elif isinstance(rule, KSet) and rule.Rel != "<=":
        return subEval(Theta(r), k) / k if k > 0 else 0.0
    elif isinstance(rule, Theta):
        return k * subEval(rule.SubRule, k)
    elif isinstance(rule, Delta):
        dlt = 0.0
        for i in range(1, k+1):
            dlt += rule.Function(i) * subEval(rule.SubRule, k/i) if k % i == 0 else 0.0
        return dlt
    else: raise Exception("Unsupported rule " + str(rule))