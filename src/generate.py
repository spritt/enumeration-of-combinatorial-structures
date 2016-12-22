from rules import *

def EnumerateFromStandardForm(rules, n, v):
    t = {}
    for k in range(n+1):
        for r in rules:
            t = evaluateRule(r, k, t, v)
    return t

def evaluateRule(rule, k, table, vals):
    # initialize
    if k not in table:
        table[k] = {}
    # 0 if k < valuation
    if len(rule.Value) == 1 and k < vals[rule.Value]:
        table[k][rule.Value] = 0.0
    elif len(rule.Value) == 2 and k < vals[rule.Value[1]]:
         table[k][rule.Value] = 0.0
    # A = B + C
    elif isinstance(rule, Union):
        table[k][rule.Value] = table[k][rule.SubRule1] + table[k][rule.SubRule2]
    # A = B * C
    elif isinstance(rule, Product):
        table[k][rule.Value] = 0.0
        for i in range(0,k+1):
            if rule.SubRule1 not in table[i]:
                continue
            if rule.SubRule2 not in table[k-i]:
                continue
            table[k][rule.Value] += table[i][rule.SubRule1] * table[k-i][rule.SubRule2]
    # A = Z
    elif isinstance(rule, Atom):
        table[k][rule.Value] = 1.0 if rule.Size == k else 0.0
    # A = Set(B), only used for k = 0
    elif isinstance(rule, Set) or (isinstance(rule, KSet) and rule.Rel == "<="):
        if k == 0: table[k][rule.Value] = 1.0
        return table
    else: raise Exception('Unsupported rule')
    # for every rule R, tabulate Theta(R) and vice versa
    if len(rule.Value) == 2 and rule.Value[1] not in table[k]:
        table[k][rule.Value[1]] = float(table[k][rule.Value]) / k if k > 0 else 0.0
    elif len(rule.Value) == 1 and 'T' + rule.Value not in table[k]:
        table[k]['T' + rule.Value] = k * float(table[k][rule.Value])
    # done
    return table