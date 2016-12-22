import copy
from rules import *

def ConvertToStandardForm(eq):
    r, _ = convert(eq, {}, 65)
    return r.values()

# helper function for ConvertToStandardForm
def convert(op, rules, v):
    if isinstance(op, Set):
        op1 = op.SubRule
        evalSub = False
        val = None
        if isinstance(op1, Union) or isinstance(op1, Product):
            val = chr(v)
            v += 1
            op1.Value = val
            evalSub = True
        elif isinstance(op1, Atom):
            for r in rules.values():
                if isinstance(r, Atom) and r.Size == op1.Size:
                    val = r.Value
                    break
            if val == None:
                val = chr(v)
                v += 1
                op1.Value = val
                rules[val] = op1
        else: val = op1
        op.SubRule = val
        rules[op.Value] = op
        rules['T' + op.Value] = Product('T' + op.Value, op.Value, 'T' + val)
        if evalSub: rules, v = convert(op1, rules, v)
    elif isinstance(op, Sequence):
        op1 = op.SubRule
        evalSub = False
        val = None
        if isinstance(op1, Union) or isinstance(op1, Product):
            val = chr(v)
            v += 1
            op1.Value = val
            evalSub = True
        elif isinstance(op1, Atom):
            for r in rules.values():
                if isinstance(r, Atom) and r.Size == op1.Size:
                    val = r.Value
                    break
            if val == None:
                val = chr(v)
                v += 1
                op1.Value = val
                rules[val] = op1
        else: val = op1
        # A = Seq(B) -> A = 1 + A*B <- add rule for A*B
        ab = chr(v)
        v += 1
        rules[ab] = Product(ab, op.Value, val)
        # A = Seq(B) -> A = 1 + A*B <- add rule for 1
        zero = None
        for r in rules.values():
            if isinstance(r, Atom) and r.Size == 0:
                zero = r.Value
                break
            if zero == None:
                zero = chr(v)
                v += 1
                rules[zero] = Atom(zero, 0)
        # A = Seq(B) -> A = 1 + A*B <- complete rule     
        rules[op.Value] = Union(op.Value, zero, ab)
        if evalSub: rules, v = convert(op1, rules, v)
    elif isinstance(op, Cycle):
        op1 = op.SubRule
        evalSub = False
        val = None
        if isinstance(op1, Union) or isinstance(op1, Product):
            val = chr(v)
            v += 1
            op1.Value = val
            evalSub = True
        elif isinstance(op1, Atom):
            for r in rules.values():
                if isinstance(r, Atom) and r.Size == op1.Size:
                    val = r.Value
                    break
            if val == None:
                val = chr(v)
                v += 1
                op1.Value = val
                rules[val] = op1
        else: val = op1
        # A = Cyc(B) -> Theta(A) = C * Theta(B) <- add rule for C
        seq = chr(v)
        v += 1
        rules, v = convert(Sequence(seq, val), rules, v)
        # A = Seq(B) -> Theta(A) = C * Theta(B) <- complete rule     
        rules['T' + op.Value] = Product('T' + op.Value, seq, 'T' + val)
        if evalSub: rules, v = convert(op1, rules, v)
    elif isinstance(op, Union) or isinstance(op, Product):
        op1, op2 = (op.SubRule1, op.SubRule2)
        val1, val2 = (None, None)
        evalLeft, evalRight = (False, False)
        if isinstance(op1, Product) or isinstance(op1, Union):
            for r in rules.values():
                rSub = copy.deepcopy(r)
                if isinstance(rSub, Union) or isinstance(rSub, Product):
                    if rSub.SubRule1 in rules:
                        if isinstance(rules[rSub.SubRule1], Atom):
                            rSub.SubRule1 = rules[rSub.SubRule1]
                    if rSub.SubRule2 in rules:
                        if isinstance(rules[rSub.SubRule2], Atom):
                            rSub.SubRule2 = rules[rSub.SubRule2]
                if rSub == op1:
                    val1 = r.Value
                    break
            if val1 == None: 
                val1 = chr(v)
                v += 1
                evalLeft = True
        elif isinstance(op1, Atom):
            for r in rules.values():
                if isinstance(r, Atom) and r.Size == op1.Size:
                    val1 = r.Value
                    break
            if val1 == None:
                val1 = chr(v)
                v += 1
                op1.Value = val1
                rules[val1] = op1
        elif isinstance(op1, Set) or isinstance(op1, KSet) or isinstance(op1, Sequence) or isinstance(op1, Cycle):
            val1 = chr(v)
            v += 1
            rules[val1] = op1
            evalLeft = True
        else: val1 = op1
        if isinstance(op2, Product) or isinstance(op2, Union):
            for r in rules.values():
                rSub = copy.deepcopy(r)
                if isinstance(rSub, Union) or isinstance(rSub, Product):
                    if rSub.SubRule1 in rules:
                        if isinstance(rules[rSub.SubRule1], Atom):
                            rSub.SubRule1 = rules[rSub.SubRule1]
                    if rSub.SubRule2 in rules:
                        if isinstance(rules[rSub.SubRule2], Atom):
                            rSub.SubRule2 = rules[rSub.SubRule2]
                if rSub == op2:
                    val2 = r.Value
                    break
            if val2 == None: 
                val2 = chr(v)
                v += 1
                evalRight = True
        elif isinstance(op2, Atom):
            for r in rules.values():
                if isinstance(r, Atom) and r.Size == op2.Size:
                    val2 = r.Value
                    break
            if val2 == None:
                val2 = chr(v)
                v += 1
                op2.Value = val2
                rules[val2] = op2
                rules[val2] = op2
        elif isinstance(op2, Set) or isinstance(op2, KSet) or isinstance(op2, Sequence) or isinstance(op2, Cycle):
            val2 = chr(v)
            v += 1
            #rules[val2] = op2
            evalRight = True
        else: val2 = op2
        op.SubRule1 = val1
        op.SubRule2 = val2
        rules[op.Value] = op # rules += [op]
        if evalLeft:
            op1.Value = val1
            rules, v = convert(op1, rules, v)
        if evalRight:
            op2.Value = val2
            rules, v = convert(op2, rules, v)
    return rules, v