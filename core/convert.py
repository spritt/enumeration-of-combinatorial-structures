import copy, math
from rules import *
from tools.util import *

def ConvertToStandardForm(eqs, labeled=True):
    v = 1
    r = {}
    for eq in eqs:
        r, v = convert(eq, r, v, labeled)
    for k,v in r.iteritems():
        print v
    return r

# helper function for ConvertToStandardForm
def convert(op, rules, v, labeled=True):
    if isinstance(op, Set):
        return convertSet(op, rules, v, labeled) if labeled else convertSetUnlabeled(op, rules, v, labeled)
    elif isinstance(op, KSet):
        return convertKSet(op, rules, v, labeled) if labeled else convertKSetUnlabeled(op, rules, v, labeled)
    elif isinstance(op, Sequence):
        return convertSequence(op, rules, v, labeled)
    elif isinstance(op, KSequence):
        return convertKSequence(op, rules, v, labeled)
    elif isinstance(op, Cycle):
        return convertCycle(op, rules, v, labeled) if labeled else convertCycleUnlabeled(op, rules, v, labeled)
    elif isinstance(op, KCycle):
        return convertKCycle(op, rules, v, labeled) if labeled else convertKCycleUnlabeled(op, rules, v, labeled)
    elif isinstance(op, Union) or isinstance(op, Product):
        return convertBinary(op, rules, v, labeled)
    elif isinstance(op, Atom):
        return {op.Value: op}, v
    else:
        raise Exception('Unsupported rule')

def assign(v):
    v += 1
    return "T" + str(v - 1), v

# helper function
def createThetaRule(rules, v, val):
    subVal = None
    for r in rules.values():
        if isinstance(r, Theta) and r.SubRule == val:
            subVal = r.Value
            break
    if subVal == None:
            subVal, v = assign(v)
            rules[subVal] = Theta(subVal, val)
    return rules, v, subVal

# binary exponentiation for sequences
def exp(rules, v, val, n):
    subVal = val
    if n == 1:
        return rules, v, subVal
    elif n == 0:
        return createAtomRule(rules, v, 0)
    elif n % 2 == 0:
        subVal, v = assign(v)
        rules[subVal] = Product(subVal, val, val)
        return exp(rules, v, subVal, n / 2)
    else:
        subVal, v = assign(v)
        rules[subVal] = Product(subVal, val, val)
        rules, v, subVal = exp(rules, v, subVal, (n - 1) / 2)
        subVal2, v = assign(v)
        rules[subVal2] = Product(subVal2, val, subVal)
        return rules, v, subVal2

# helper function
def createDeltaRule(rules, v, val, fun):
    subVal = None
    #for r in rules.values():
    #    if isinstance(r, Delta) and r.SubRule == val:
    #        subVal = r.Value
    #        break
    if subVal == None:
        subVal, v = assign(v)
        rules[subVal] = Delta(subVal, val, fun)
    return rules, v, subVal

# helper function
def createAtomRule(rules, v, size):
    atom = None
    for r in rules.values():
        if isinstance(r, Atom) and r.Size == size:
            atom = r.Value
            break
    if atom == None:
        atom, v = assign(v)
        rules[atom] = Atom(atom, 0)
    return rules, v, atom

#helper function
def convertSubRule(rules, v, op1):
    evalSub = False
    val = None
    if isinstance(op1, Union) or isinstance(op1, Product):
        val, v = assign(v)
        op1.Value = val
        evalSub = True
    elif isinstance(op1, Atom):
        for r in rules.values():
            if isinstance(r, Atom) and r.Size == op1.Size:
                val = r.Value
                break
        if val == None:
            val, v = assign(v)
            op1.Value = val
            rules[val] = op1
    else: val = op1
    return rules, v, op1, val, evalSub

def convertSequence(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    # A = Seq(B) -> A = 1 + A*B <- add rule for A*B
    ab, v = assign(v)
    rules[ab] = Product(ab, op.Value, val)
    # A = Seq(B) -> A = 1 + A*B <- add rule for 1
    rules, v, zero = createAtomRule(rules, v, 0)
    # A = Seq(B) -> A = 1 + A*B <- complete rule     
    rules[op.Value] = Union(op.Value, zero, ab)
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertKSequence(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    if op.Rel == "=": # B^k
        if op.Card == 0:
            rules[op.Value] = Atom(op.Value, 0)
        else:
            rules, v, subVal = exp(rules, v, val, op.Card - 1)
            rules[op.Value] = Product(op.Value, val, subVal)
        #rules[subVal].Value = op.Value
        #rules[op.Value] = rules[subVal]; del rules[subVal]
    elif op.Rel == ">=": # Seq(B) * B^k
        rules, v, val = exp(rules, v, val, op.Card)
        newVal, v = assign(v)
        rules, v = convert(Sequence(newVal, op1), rules, v, labeled)
        rules[op.Value] = Product(op.Value, val, newVal)
    elif op.Rel == "<=": # 1 + B + B*B + B*B*B + ... + B^k
        k = op.Card
        rules, v, yval = createAtomRule(rules, v, 0)
        xval, v = assign(v)
        rules[op.Value] = Union(op.Value, yval, xval)
        for i in range(2, k+1):
            xvalNew, v = assign(v)
            yvalNew = val
            if i > 2:
                yvalNew, v = assign(v)
                rules[yvalNew] = Product(yvalNew, yval, val)
            rules[xval] = Union(xval, yvalNew, xvalNew)
            xval = xvalNew
            yval = yvalNew
        rules[xval] = Product(xval, yval, val)
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
    rules, v, subValDelta = createDeltaRule(rules, v, subValTheta, lambda x : 1)
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
            newVal, v = assign(v)
            rules, v = convert(KSet(newVal, val, op.Rel, op.Card - 1), rules, v, labeled)
        rules[op.Value] = op
    elif op.Rel == "<=":
        newVal, v = assign(v)
        if op.Card > 2:
            rules, v = convert(KSet(newVal, val, op.Rel, op.Card - 1), rules, v, labeled)
        else:
            rules, v, zero = createAtomRule(rules, v, 0)
            rules[newVal] = Union(newVal, zero, val)
        rules[op.Value] = op
    elif op.Rel == ">=":
        newVal, v = assign(v)
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

def convertKSetUnlabeled(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    k = op.Card
    xvals = [assign(v) for i in range(k)]
    yvals = [assign(v) for i in range(k)]
    ###### First create and store the terms ######
    for i in range(1,k+1):
        ###### Create Delta term ##########
        # create new Theta subrule unless it already exists
        rules, v, subValTheta = createThetaRule(rules, v, val)
        # create new Delta subrule unless it already exists
        if op.Rel == ">=" and i == k:
            rules, v, subValDelta = createDeltaRule(rules, v, subValTheta, lambda x, y=i : 1 if x >= y else 0)
        else:
            rules, v, subValDelta = createDeltaRule(rules, v, subValTheta, lambda x, y=i : 1 if x == y else 0)
        yvals[i-1] = subValDelta
        ###### Create recurrent term ######
        if k - i == 1: 
            if op.Rel == "=":
                subVal = val
            elif op.Rel == "<=":
                subVal, v = assign(v)
                rules, v, zero = createAtomRule(rules, v, 0)
                rules[subVal] = Union(subVal, zero, val)
            elif op.Rel == ">=":
                subVal, v = assign(v)
                rules, v = convert(KSet(subVal, val, op.Rel, k - i), rules, v, labeled)
        elif k - i == 0:
            if op.Rel == ">=":
                subVal, v = assign(v)
                rules, v = convert(Set(subVal, val), rules, v, labeled)
            else:
                rules, v, subVal = createAtomRule(rules, v, 0)
        else:
            subVal, v = assign(v)
            rules, v = convert(KSet(subVal, val, op.Rel, k - i), rules, v, labeled)
        xvals[i-1] = subVal
    ###### Now sum the terms ######
    if k == 1 and op.Rel == ">=":
        rules[Theta(op.Value)] = Product(Theta(op.Value), xvals[0], yvals[0])
    else:
        sumVal, v = assign(v)
        rules[sumVal] = Product(sumVal, xvals[0], yvals[0]) # first term
    for i in range(1,k):
        ###### Product of delta term and recurrent term ######
        prodVal, v = assign(v)
        rules[prodVal] = Product(prodVal, xvals[i], yvals[i])
        if i < k-1: # iteratively sum
            newVal, v = assign(v)
            rules[newVal] = Union(newVal, sumVal, prodVal)
            sumVal = newVal
        else: # the complete rule
            rules[Theta(op.Value)] = Union(Theta(op.Value), sumVal, prodVal)
    rules[op.Value] = op
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertCycle(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # A = Cyc(B) -> Theta(A) = C * Theta(B) <- add rule for C
    seq, v = assign(v)
    rules, v = convert(Sequence(seq, val), rules, v, labeled)
    # A = Cyc(B) -> Theta(A) = C * Theta(B) <- add rule for Theta(B)
    rules, v, thetaVal = createThetaRule(rules, v, val)
    # A = Seq(B) -> Theta(A) = C * Theta(B) <- complete rule     
    rules[Theta(op.Value)] = Product(Theta(op.Value), seq, thetaVal)
    rules[op.Value] = op
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertKCycle(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # A = Cyc_k(B) -> Theta(A) = Seq_{k-1}(B) * Theta(B) <- add rule for Seq_{k-1}(B)
    seq, v = assign(v)
    rules, v = convert(KSequence(seq, val, op.Rel, op.Card - 1), rules, v, labeled)
    # A = Cyc_k(B) -> Theta(A) = Seq_{k-1}(B) * Theta(B) <- add rule for Theta(B)
    rules, v, thetaVal = createThetaRule(rules, v, val)
    # A = Cyc_k(B) -> Theta(A) = Seq_{k-1}(B) * Theta(B) <- complete rule
    rules[Theta(op.Value)] = Product(Theta(op.Value), seq, thetaVal)
    rules[op.Value] = op
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertCycleUnlabeled(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    # Theta(A) = C * Theta(B) <- add rule for C = Seq(B)
    seqVal, v = assign(v)
    rules, v = convert(Sequence(seqVal, val), rules, v, labeled)
    # Theta(A) = C * Theta(B) <- add rule for Theta(B)
    rules, v, thetaVal = createThetaRule(rules, v, val)
    # Theta(A) = C * Theta(B)  
    prodVal, v = assign(v)
    rules[prodVal] = Product(prodVal, seqVal, thetaVal)
    # Theta(A) = Delta(C * Theta(B))
    rules[Theta(op.Value)] = Delta(Theta(op.Value), prodVal, lambda x: tot(x))
    rules[op.Value] = op
    if evalSub: rules, v = convert(op1, rules, v, labeled)
    return rules, v

def convertKCycleUnlabeled(op, rules, v, labeled):
    op1 = op.SubRule
    rules, v, op1, val, evalSub = convertSubRule(rules, v, op1)
    op.SubRule = val
    k = op.Card
    if op.Rel == "=" or op.Rel == "<=":  
        sumVal = val
        # Theta(A) = C * Theta(B) <- add rule for Theta(B)
        rules, v, thetaVal = createThetaRule(rules, v, val)
        for j in range(1,k+1):
            if op.Rel == "=" and k % j != 0:
            #if k % j != 0:
                continue
            ###### create the term ######
             # Theta(A) = C * Theta(B) <- add rule for C = Seq_k(B)
            seqVal, v = assign(v)
            if op.Rel == "=":
                rules, v = convert(KSequence(seqVal, val, "=", k/j - 1), rules, v, labeled)
            elif op.Rel == "<=":
                rules, v = convert(KSequence(seqVal, val, "<=", int(math.floor(k/j - 1))), rules, v, labeled) #########
                #rules, v = convert(KSequence(seqVal, val, "<=", k/j - 1), rules, v, labeled)
            # Theta(A) = C * Theta(B)  
            prodVal, v = assign(v)
            rules[prodVal] = Product(prodVal, seqVal, thetaVal)
            # special case for k = 1
            if k == 1:
                rules[Theta(op.Value)] = Delta(Theta(op.Value), prodVal, lambda x, y=j : tot(y) if x == y else 0)
                continue
            # otherwise, create Delta rule
            rules, v, deltaVal = createDeltaRule(rules, v, prodVal, lambda x, y=j : tot(y) if x == y else 0)
            ###### continue the sum ######
            if j == k:
                rules[Theta(op.Value)] = Union(Theta(op.Value), sumVal, deltaVal)
            elif j == 1:
                sumVal = deltaVal
            else:
                newVal, v = assign(v)
                rules[newVal] = Union(newVal, sumVal, deltaVal)
                sumVal = newVal
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
            val1, v = assign(v)
            evalLeft = True
    elif isinstance(op1, Atom):
        for r in rules.values():
            if isinstance(r, Atom) and r.Size == op1.Size:
                val1 = r.Value
                break
        if val1 == None:
            val1, v = assign(v)
            op1.Value = val1
            rules[val1] = op1
    elif isinstance(op1, Set) or isinstance(op1, KSet) or isinstance(op1, Sequence) or isintance(op1, KSequence) or isinstance(op1, Cycle) or isinstance(op1, KCycle):
        val1, v = assign(v)
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
            val2, v = assign(v)
            evalRight = True
    elif isinstance(op2, Atom):
        for r in rules.values():
            if isinstance(r, Atom) and r.Size == op2.Size:
                val2 = r.Value
                break
        if val2 == None:
            val2, v = assign(v)
            op2.Value = val2
            rules[val2] = op2
            rules[val2] = op2
    elif isinstance(op2, Set) or isinstance(op2, KSet) or isinstance(op2, Sequence) or isinstance(op2, KSequence) or isinstance(op2, Cycle) or isinstance(op2, KCycle):
        val2, v = assign(v)
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
