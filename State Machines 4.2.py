# Name: Soon Sam R Santos
# Date: March 01, 2017
# Session: 3
# State Machines 4.2.py

class SM:
    startState = None
    def start(self):
        self.state = self.startState
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o
    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]
    def run(self, n=10):
        return [self.transduce([None]*n)]
    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)
# The above state machine is just for training.
import lib601.sm as sm

class Delay(sm.SM):
    def __init__(self, val):
        self.startState = val
    def getNextValues(self, state, inp):
        return (inp, state)
D1 = Delay(100)
D2 = Delay(50)

# Cascading the two state machines.
class Cascade(sm.SM):
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        # The startState is a tuple with the state of both machines.
        # I must declare always the startState. Step will take carry of self.state.
        self.startState = (sm1.startState, sm2.startState)
    def getNextValues(self, state, inp):
        # Separating the states.
        (s1, s2) = state
        # Using the states separetadely
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        # The output of the first is the input of the second(property of Cascade Machines).
        (nextS2, o2) = self.m2.getNextValues(s2, o1)
        # Again, the next state is a tuple with both states,
        # therefore I use the states as they separetadely.
        return ((nextS1, nextS2), o2)
C = Cascade(Delay(99),Delay(22))
print C.transduce([3,8,2,4,6,5])
# [22,99,3,8,2,4]
# The output is delaying by two now.
def safeAdd(v1, v2):
    if v1 == 'undefined' or v2 == 'undefined':
        return 'undefined'
    else:
        return v1 + v2

class Increment(sm.SM):
    def __init__(self, incr):
        self.startState = 0 
        self.incr = incr
    def getNextValues(self, state, inp):
        return (safeAdd(inp, self.incr), safeAdd(inp, self.incr))
I = Increment(1)
print I.transduce([3,4,5,6,7])

#C2 = Cascade(Delay(99), Increment(10))
#print C2.transduce([1,2,3,4,5,6])
# [109, 11, 12, 13, 14, 15]
# The output is delaying by one step and the increment by 10 units.

class Parallel(sm.SM):
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (sm1.startState, sm2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, inp)
        return ((nextS1, nextS2), (o1, o2))
P = Parallel(Delay(100), Delay (50))
print P.transduce([1,2,3,4,5,6])

# If the inp is a pair of tuple my algorithm will take carry of it,
# but if it is undefined, I must split it to be (undefined, undefined).
def splitValues(v):
    if v == 'undefined':
        return ('undefined', 'undefined')
    else:
        return vars
class Parallel2(Parallel):
    # Inherit the __init__ method from parallel
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (i1, i2) = splitValues(inp)
        (nextS1, o1) = self.m1.getNextValues(s1, i1)
        (nextS2, o2) = self.m1.getNextValues(s2, i2)
        return ((nextS1, nextS2), (o1, o2))                
P2 = Parallel(Delay(100), Delay(200))
print P2.transduce([(1,10), (2,20), (3,30), (4,40)])

# Same as Parallel, but the output is the sum of both outputs
class ParallelAdd(Parallel):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, inp)
        return ((nextS1, nextS2), o1+o2)

# Feedback Composition
# Takes the output as input. Needs a Delay machine to properly work.
class Feedback(sm.SM):
    def __init__(self, sm):
        self.m = sm
        # The startState of the fb is just the same as of the machine.
        self.startState = self.m.startState
    def getNextValues(self, state, inp):
        # This line is just to generate an output, which is the starting state of the Delay Machine (in the example below).
        (ignore, o) = self.m.getNextValues(state, 'undefined')
        # Then I use the output above to be the input of this one.
        (nextS, ignore) = self.m.getNextValues(state, o)
        # The nextState is 2, the output is 1, therefore I am delaying by one step to show the output.
        return (nextS, o)

# It will only work when I do the safeAdd method. I don't know where to put this method right now.
def makeCounter(init, step):
    # sm. means I am taking from the lib601.
    return sm.Feedback(sm.Cascade(Increment(step), sm.Delay(init)))
c = makeCounter(3,2)
print c.run()
# [3,5,7,9,11,13,15]... the default value is 10 steps.
print sm.Feedback(sm.Cascade(sm.Delay(3), Increment(2))).run()
# [5,7,9,11,13,15,17]...

class Adder(sm.SM):
    def getNextState(self, state, inp):
        (i1, i2) = splitValues(inp)
        return safeAdd(i1, i2)
# safeAdd and splitValue in case I get 'undefined'.
# This simple machine just return as the nextstate and output the sum of the inputs.

# The fibonnaci is the feedback of the Cascade: 1 - of the parallel of Delay by one step with Delay by two steps, 2 - with the Adder.
# Sequence of the number inside the Delay machines
# 0,0,1  This sequence give me the fibonacci beginning with 1,1,2,3
# 1,1,0  This sequence give me the fibonacci beginning with 1,2,3
fib = sm.Feedback(sm.Cascade(sm.Parallel(sm.Delay(0), sm.Cascade(sm.Delay(0), sm.Delay(1))), Adder()))
fib_2 = sm.Feedback(sm.Cascade(sm.Parallel(sm.Delay(1), sm.Cascade(sm.Delay(1), sm.Delay(0))), Adder()))
print fib.run(20)  # run is inputing 20 times None. As feedback doesn't need input.

class Wire(sm.SM):
    def getNextState(self, state, inp):
        return inp

# Define fibonacci as a composition involving only two delay components and an adder.
# new_fib = sm.Feedback(sm.Cascade(sm.Cascade(sm.Delay(1), sm.Delay(0)), Adder()))
# print new_fib.run(20)

def safeMul(v1, v2):
    if v1 == 'undefined' or v2 == 'undefined':
        return 'undefined'
    else:
        return v1*v2
class Multiplier(sm.SM):
    def getNextState(self, state, inp):
        return safeMul(inp,2)

def Double(init):
    return sm.Feedback(sm.Cascade(Multiplier(), sm.Delay(init)))
D2 = Double(2)
print D2.run(20)
# Feedback: the output is the next input with no directly relationship between them, that's why I use the Delay machine.

class Square(sm.SM):
    def getNextState(self, state, inp):
        return safeMul(inp, inp)

def Square_Machine(init):
    return sm.Feedback(sm.Cascade(Square(), Delay(init)))
# If I plug here 1, the square of 1 is always 1. Therefore all the outputs will be 1.
S = Square_Machine(2)
# If i run with a big number like 20, the program will not hold the Long numbers.
print S.run(7)

# Feedback2
# It receives as input, the output and another input
class Feedback2(Feedback):
    # Inherits the __init__ method.
    def getNextValues(self, state, inp):
        (ignore, o) = self.m.getNextValues(state, (inp, 'undefined'))
        # Receiving as the input, the output and a new input.
        # This machine does not ignore the inputs.
        (nextS, ignore) = self.m.getNextValues(state,(inp, o))
'''
class FeedbackAdd(sm.SM):
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (self.m1.startState, self.m2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = splitValues(state)
        (ignore, o1) = self.m1.getNextValues(s1, (inp, 'undefined'))
        (nextS2, o2) = self.m2.getNextValues(s2, o1)
        (ignore, o3) = self.m1.getNextValues(state, (inp, o2))
        return (nextS2, o3)
newM = FeedbackAdd(sm.R(0), sm.Wire())
print newM.transduce([0,1,2,3,4,5,6,7,8,9])
'''
newM = sm.FeedbackAdd(sm.R(0), sm.Wire())
print newM.transduce([0,1,2,3,4,5,6,7,8,9])
class Multiplier(sm.SM):
    def getNextState(self, state, inp):
        (i1, i2) = splitValues(inp)
        return safeMul(i1,i2)
# Factorial Sequence.
# I am Feedingback 2 the cascade of multiplier and delay. The second input is the makecounter.
# By the way the counter will multiply the previous result.

print sm.Cascade(makeCounter(1,1), sm.Feedback2(sm.Cascade(Multiplier(),sm.Delay(1)))).run()
# Construct several small things and build such great things. This is a tricky algorithm, but I could do this in just one line,
# because I have hundreds of lines helping me with the several state machines I am using.

# Plant and Controllers, a better explanation in my notebook.
k = -1.5
dDesired = 1.0
class WallController(sm.SM):
    startState = 0 
    def getNextState(self, state, inp): # inp is the current distance.
        # This return the velocity.
        return safeMul(k,safeAdd(dDesired,safeMul(-1,inp))) # -1 is just to do a subtraction using safeAdd instead of Subtract.
deltaT = 0.1
class WallWorld(sm.SM):
    startState = 5
    def getNextValues(self, state, inp): # inp is the current velocity
        # This return the distance.
        # state is the distance from the wall.
        # nextState is calculating the next distance, while state is outputing the previous distance. It delays by one time step.
        return (state - deltaT*inp, state)
def coupledMachine(m1, m2):
    return sm.Feedback(sm.Cascade(m1,m2))
# The controller output the velocity to be the input of the World.
# wallSim = coupledMachine(WallController(), WallWorld())
# print wallSim.run()

# 4.2.6 - Switch
# Two machines in parallel, decides whether to send the input to one or another in every input. So only one machine has its state updated on each step.
# We maintain the state of both machines. The getNextValues gets a new state and an output from the appropriate machine, it needs to pass throught the old state
# for the constituent machine that was not updated this time.
class Accumulator(sm.SM):
    startState = 0
    def getNextState(self, state, inp):
        # I want to store all the inputs.
        return state + inp

class Switch(SM):
    def __init__(self, condition, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.condition = condition
        self.startState = (self.m1.startState, self.m2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = state
        # If the condition is satisfied.
        if self.condition(inp):
            # I execute for the first machine.
            (ns1, o) = self.m1.getNextValues(s1, inp)
            # Return the newstate, and the old state of the other machine.
            return ((ns1, s2), o)
        else:
            (ns2, o) = self.m2.getNextValues(s2, inp)
            return ((s1, ns2), o)

# Multiplex.
# Now I want to do as Switch but I want to update the state of each machine in every step but the condition will be useful to tell what output I will show.

class Multiplex(Switch):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (ns1, o1) = self.m1.getNextValues(s1, inp)
        (ns2, o2) = self.m2.getNextValues(s2, inp)
        if self.condition(inp):
            return ((ns1, ns2), o1)
        else:
            return ((ns1, ns2), o2)
# TestCases
# This don't output the accumulation of all inputs.
m1 = Switch(lambda inp: inp>100, Accumulator(), Accumulator())
print m1.transduce([2,3,4,200,300,400,1,2,3])
# This doest output the accumulation of all inputs.
m2 = Multiplex(lambda inp: inp>100, Accumulator(), Accumulator())
print m2.transduce([2,3,4,200,300,400,1,2,3])
