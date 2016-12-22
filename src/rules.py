class Union:
    def __init__(self, *args): # args[0] = args[1] + args[2]
        self.Type = 'Union'
        if len(args) == 3:
            self.Value = args[0]
            self.SubRule1 = args[1]
            self.SubRule2 = args[2]
        elif len(args) == 2:
            self.Value = ''
            self.SubRule1 = args[0]
            self.SubRule2 = args[1]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, Union) and \
            self.SubRule1 in (other.SubRule1, other.SubRule2) and \
            self.SubRule2 in (other.SubRule1, other.SubRule2) and \
            other.SubRule1 in (self.SubRule1, self.SubRule2) and \
            other.SubRule2 in (self.SubRule1, self.SubRule2)
    def __str__(self):
        return self.Value + " = " + self.SubRule1 + " + " + self.SubRule2

class Product:
    def __init__(self, *args): # args[0] = args[1] * args[2]
        self.Type = 'Product'
        if len(args) == 3:
            self.Value = args[0]
            self.SubRule1 = args[1]
            self.SubRule2 = args[2]
        elif len(args) == 2:
            self.Value = ''
            self.SubRule1 = args[0]
            self.SubRule2 = args[1]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, Product) and \
            self.SubRule1 in (other.SubRule1, other.SubRule2) and \
            self.SubRule2 in (other.SubRule1, other.SubRule2) and \
            other.SubRule1 in (self.SubRule1, self.SubRule2) and \
            other.SubRule2 in (self.SubRule1, self.SubRule2)
    def __str__(self):
        return self.Value + " = " + self.SubRule1 + " * " + self.SubRule2
            
class Sequence:
    def __init__(self, *args): # args[0] = seq(args[1])
        self.Type = 'Sequence'
        if len(args) == 2:
            self.Value = args[0]
            self.SubRule = args[1]
        elif len(args) == 1:
            self.Value = ''
            self.SubRule = args[0]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, Sequence) and \
            self.SubRule == other.SubRule
    def __str__(self):
        return self.Value + " = Seq(" + self.SubRule + ")"
        
class Set:
    def __init__(self, *args): # args[0] = set(args[1])
        self.Type = 'Set'
        if len(args) == 2:
            self.Value = args[0]
            self.SubRule = args[1]
        elif len(args) == 1:
            self.Value = ''
            self.SubRule = args[0]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, Set) and \
            self.SubRule == other.SubRule
    def __str__(self):
        return self.Value + " = Set(" + self.SubRule + ")"
    
class KSet:
    def __init__(self, *args): # args[0] = set(args[1])
        self.Type = 'KSet'
        if len(args) == 4:
            self.Value = args[0]
            self.SubRule = args[1]
            self.Rel = args[2]
            self.Card = args[3]
        elif len(args) == 3:
            self.Value = ''
            self.SubRule = args[0]
            self.Rel = args[1]
            self.Card = args[2]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, KSet) and \
            self.SubRule == other.SubRule
    def __str__(self):
        return self.Value + " = Set(" + self.SubRule + ", k " + self.Rel + " " + str(self.Card) + ")"
    
class Cycle:
    def __init__(self, *args): # args[0] = set(args[1])
        self.Type = 'Cycle'
        if len(args) == 2:
            self.Value = args[0]
            self.SubRule = args[1]
        elif len(args) == 1:
            self.Value = ''
            self.SubRule = args[0]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, Cycle) and \
            self.SubRule == other.SubRule
    def __str__(self):
        return self.Value + " = Cyc(" + self.SubRule + ")"

class Atom:
    def __init__(self, *args):
        self.Type = 'Atom'
        if len(args) == 2:
            self.Value = args[0]
            self.Size = args[1]
        elif len(args) == 1:
            self.Value = ''
            self.Size = args[0]
        else: raise Exception('Invalid parameters')
    def __eq__(self, other):
        return isinstance(other, Atom) and self.Size == other.Size
    def __str__(self):
        return self.Value + " = Z^" + str(self.Size)