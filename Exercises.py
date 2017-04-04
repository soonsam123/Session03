# Name: Soon Sam R Santos
# Date: March 04, 2017
# Session: 3
# Cascading_Machines.py

# ************************Problem WK.3.1.2************************
import lib601.sm as sm

def splitValues(v):
    if v == 'undefined':
        return 'undefined'
    else:
        return v

# The inp is received for the first machine, then the output is the input for the second machine.
class Cascade(sm.SM):
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (self.m1.startState, self.m2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = splitValues(state)
        (nextS1, o1) = self.m1.getNextValues(s1, inp)
        (nextS2, o2) = self.m2.getNextValues(s2, o1)

# ************************Problem WK.3.1.3************************
# Part1
# Applies a given function to the input and returns the result as the output
class PureFunction(sm.SM):
    def __init__(self, f):
        self.f = f
    # Doesn't need to change the state.
    def getNextValues(self, state, inp):
        return (state ,self.f(inp))

# ************************Problem WK.3.1.4************************

class BA1(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        if inp != 0:
            newState = (state * 1.02) + (inp - 100)
        else:
            newState = (state * 1.02)
        return (newState, newState)
class BA2(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        newState = (state * 1.01) + inp 
        return (newState, newState)

ba1 = BA1()
ba2 = BA2()
# Same input for both machines
Max = sm.Parallel(ba1,ba2)
# Output a tuple with two outputs, from account 1 and 2.
# This function return the bigger value.
def Bigger(v):
    (v1, v2) = v
    if v1>=v2:
        return v1
    else:
        return v2
Max_new = PureFunction(Bigger)
# The tuple from Max will be outputed to be the input of the PureFunction which contains the Bigger function. 
Maximize = sm.Cascade(Max,Max_new)
print Maximize.transduce([100,200])

# Part2

def check_account(val):
    (v1, v2) = val
    if (v1>=3000 or v1<=-3000) and -3000<v2<3000:
        return (v1,v2)
    else:
        return (v2,v1)
def get_result(val):
    (v1, v2) = val
    return v1+v2
# Receive two inputs, check which should be the first or the second and output for the parallel2, this output a tuple with the two result which is cascade
# to another PureFunction that calculate the sum of the two values in the tuple.
switchAccount = sm.Cascade(sm.Cascade(sm.PureFunction(check_account), sm.Parallel2(ba1, ba2)),sm.PureFunction(get_result))
print switchAccount.transduce([(2500,3500),(-150,-3000)])

# ************************WK.3.1.5 : Sequential Combination (4.3)************************
# Part 1 - Sum Machine
class SumTSM(sm.SM):
    startState = 0 
    def getNextValues(self, state, inp):
        return (state + inp, state + inp)
    def done(self, state):
        return state > 100
print SumTSM().transduce([10,20,30,40,50,60,70,80])

# Part 2 - Some machine
fourTimes = sm.Repeat(SumTSM(), 4)
print fourTimes.transduce(range(1000), verbose = True)

# Part 3 - Counting Machine
class CountUpTo(sm.SM):
    startState = 0 
    def __init__(self, until):
        self.until = until
    def getNextValues(self, state, inp):
        # Increment 1 by each step. Starts as 0.
        return (state + 1, state + 1)
    def done(self, state):
        # Finish when the state is equal to the specified number. 
        return state == self.until
m = CountUpTo(3)
print m.run(20)

# Part 4 - Multiple Counting machine
def makeSequenceCounter(nums):
    # Sequence of machines, The first counts up to the first number of the list and so on until the last number.
    return sm.Sequence([CountUpTo(num) for num in nums])
m = makeSequenceCounter([2,5,3])
print m.run(20)

# ************************WK.3.1.6: Feedback SM************************
def negation(Bool):
    return not Bool
negate = sm.PureFunction(negation)
# Alternating between True and False for any input. Beginning with True.
# Feedback to return the last output to be the next input.
# Cascade Delay with negate, The output of Delay will go to negate.
alternating = sm.Feedback(sm.Cascade(sm.Delay(False),negate))
print alternating.run(verbose = True)
