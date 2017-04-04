import copy
from rules import *

def ConvertToStandardForm(eq, labeled=True):
    r, _ = convert(eq, {}, 65, labeled)
    for k,v in r.iteritems():
        print v
    return r

# helper function for ConvertToStandardForm
def convert(op, rules, v, labeled=True):
    if isinstance(op, Set):
        return convertSet(op, rules, v, labeled) if labeled else convertSetUnlabeled(op, rules, v, labeled)
    elif isinstance(op, KSet):
        return convertKSet(op, rules, v, labeled)
    elif isinstance(op, Sequence):
        return convertSequence(op, rules, v, labeled)
    elif isinstance(op, Cycle):
        return convertCycle(op, rules, v, labeled) if labeled else convertCycleUnlabeled(op, rules, v, labeled)
    elif isinstance(op, Union) or isinstance(op, Product):
        return convertBinary(op, rules, v, labeled)
    else:
        raise Exception('Unsupported rule')

# helper function
def createThetaRule(rules, v, val):
    subVal = None
    for r in rules.values():
        if isinstance(r, Theta) and r.SubRule == val:
            subVal = r.Value
            break
    if subVal == None:
            subVal = chr(v)
            v += 1
            rules[subVal] = Theta(subVal, val)
    return rules, v, subVal

# helper function
def createDeltaRule(rules, v, val):
    subVal = None
    for r in rules.values():
        if isinstance(r, Delta) and r.SubRule == val:
            subVal = r.Value
            break
    if subVal == None:
            subVal = chr(v)
            v += 1
            rules[subVal] = Delta(subVal, val)
    return rules, v, subVal

# helper function
def createAtomRule(rules, v, size):
    atom = None
    for r in rules.values():
        if isinstance(r, Atom) and r.Size == size:
            atom = r.Value
            break
    if atom == None:
        atom = chr(v)
        v += 1
        rules[atom] = Atom(atom, 0)
    return rules, v, atom

#helper function
def convertSubRule(rules, v, op1):
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
    return rules, v, op1, val, evalSub

def convertSequence(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    # A = Seq(B) -> A = 1 + A*B <- add rule for A*B
    ab = chr(v)
    v += 1
    rules[ab] = Product(ab, op.Value, val)
    # A = Seq(B) -> A = 1 + A*B <- add rule for 1
    rules, v, zero = createAtomRule(rules, v, 0)
    # A = Seq(B) -> A = 1 + A*B <- complete rule     
    rules[op.Value] = Union(op.Value, zero, ab)
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertSet(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # create new Theta subrule unless it already exists
    rules, v, subVal = createThetaRule(rules, v, val)
    # add new rules
    rules[op.Value] = op
    rules[Theta(op.Value)] = Product(Theta(op.Value), op.Value, subVal)
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertSetUnlabeled(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # create new Theta subrule unless it already exists
    rules, v, subValTheta = createThetaRule(rules, v, val)
    # create new Delta subrule unless it already exists
    rules, v, subValDelta = createDeltaRule(rules, v, subValTheta)
    # add new rules
    rules[op.Value] = op
    rules[Theta(op.Value)] = Product(Theta(op.Value), op.Value, subValDelta)
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertKSet(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    if op.Rel == "=":
        newVal = val
        if op.Card > 2:
            newVal = chr(v)
            v += 1
            rules, v = convert(KSet(newVal, val, op.Rel, op.Card - 1), rules, v, labeled)
        rules[op.Value] = op
    elif op.Rel == "<=":
        newVal = chr(v)
        v += 1
        if op.Card > 2:
            rules, v = convert(KSet(newVal, val, op.Rel, op.Card - 1), rules, v, labeled)
        else:
            rules, v, zero = createAtomRule(rules, v, 0)
            rules[newVal] = Union(newVal, zero, val)
        rules[op.Value] = op
    elif op.Rel == ">=":
        newVal = chr(v)
        v += 1
        if op.Card > 1:
            rules, v = convert(KSet(newVal, val, op.Rel, op.Card - 1), rules, v, labeled)
        else:
            rules, v = convert(Set(newVal, val), rules, v, labeled)
        rules[op.Value] = op
    # create new Theta subrule unless it already exists
    rules, v, subVal = createThetaRule(rules, v, val)
    rules[Theta(op.Value)] = Product(Theta(op.Value), newVal, subVal)    
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertCycle(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # A = Cyc(B) -> Theta(A) = C * Theta(B) <- add rule for C
    seq = chr(v)
    v += 1
    rules, v = convert(Sequence(seq, val), rules, v, labeled)
    # A = Cyc(B) -> Theta(A) = C * Theta(B) <- add rule for Theta(B)
    rules, v, subVal = createThetaRule(rules, v, val)
    # A = Seq(B) -> Theta(A) = C * Theta(B) <- complete rule     
    rules[Theta(op.Value)] = Product(Theta(op.Value), seq, subVal)
    rules[op.Value] = op
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertCycleUnlabeled(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # Theta(A) = C * Theta(B) <- add rule for C
    seq = chr(v)
    v += 1
    rules, v = convert(Sequence(seq, val), rules, v, labeled)
    # Theta(A) = C * Theta(B) <- add rule for Theta(B)
    rules, v, subVal = createThetaRule(rules, v, val)
    # Theta(A) = C * Theta(B)  
    prod = chr(v)
    v += 1
    rules[prod] = Product(prod, seq, subVal)
    # Theta(A) = CycDelta(C * Theta(B))
    rules[Theta(op.Value)] = CycDelta(Theta(op.Value), prod)
    rules[op.Value] = op
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertBinary(op, rules, v, labeled):
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
        rules, v = convert(op1, rules, v, labeled)
    if evalRight:
        op2.Value = val2
        rules, v = convert(op2, rules, v, labeled)
    return rules, v
