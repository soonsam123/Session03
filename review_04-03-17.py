import lib601.sm as sm
def safeAdd(v1, v2):
    if v1 = 'undefined' or v2 = 'undefined':
        return 'undefined'
    else:
        return v1 + v2
def safeMul(v1,v2):
    if v1 = 'undefined' or v2 = 'undefined':
        return 'undefined'
    else:
        return v1*v2
def splitValues(v1,v2):
    if v == 'undefined':
        return ('undefined','undefined')
    else:
        return v
class Delay(sm.SM):
    def __init__(self, val):
        self.startState = val
    def getNextState(self, state, inp):
        return (inp, state)

class Cascade(sm.SM):
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (self.m1.startState, self.m2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, o1)
        return ((nextS1, nextS2), o2)

class Increment(sm.SM):
    def __init__(self, incr):
        self.startState = 0 
        self.incr = incr
    def getNextState(self, state, inp):
        return safeAdd(inp, self.incr)

class Parallel(Cascade):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, inp)
        return ((nextS1, nextS2), (o1, o2))     
    
class Parallel2(Parallel):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (i1, i2) = splitValues(inp)
        (nextS1, o1) = self.m1.getNextValues(s1, i1)
        (nextS2, o2) = self.m2.getNextValues(s2, i2)
        return ((nextS1, nextS2), (o1, o2))
    
class ParallelAdd(Parallel):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, inp)
        return ((nextS1, nextS2), o1 + o2)     

class Feedback(sm.SM):
    def __init__(self, sm):
        self.m = sm
        self.startState = self.m.startState
    def getNextValues(self, state, inp):
        (ignore, o) = self.m.getNextValues(state, 'undefined')
        (nextS, ignore) = self.m.getNextValues(state, o)
        return (nextS, o)

def makeCounter(init, step):
    return sm.Feedback(sm.Cascade(Increment(step), Delay(init)))

class Adder(sm.SM):
    def getNextState(self, state, inp):
        (i1, i2) = splitValues(inp)
        return safeAdd(i1, i2)

class Wire(sm.SM):
    def getNextState(self, state, inp):
        return inp

class Multiplier(sm.SM):
    def getNextState(self, state, inp):
        return safeMul(inp,2)

class Square(sm.SM):
    def getNextState(self, state, inp):
        return safeMul(inp, inp)

class Feedback2(Feedback):
    def getNextValues(self, state, inp):
        (ignore, o) = self.m.getNextValues(state, (inp, 'undefined'))
        (nextS, ignore) = self.m.getNextValues(state, (inp, o))
        return (nextS, o)

class Accumulator(sm.SM):
    startState = 0
    def getNextState(self, state, inp):
        return state + inp

class Switch(sm.SM):
    def __init__(self, condition, sm1, sm2):
        self.condition = condition
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (self.m1.startState, self.m2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = state
        if self.condition(inp):
            (nextS1, o1) = self.m1.getNextValues(s1, inp)
            return ((nextS1, s2), o1)
        else:
            (nextS2, o2) = self.m2.getNextValues(s2, inp)
            return ((s1, nextS2), o2)
            
class Multiplex(Switch):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, inp)
        if self.condition(inp):
            return ((nextS1, nextS2), o1)
        else:
            return ((nextS1, nextS2), o2)
        
