# Name: Soon Sam R Santos
# Date: March 06, 2017
# Session 3
# State_Machines_4.3.py
import lib601.sm as sm

class ConsumeFiveValues(sm.SM):
    startState = (0,0)  # count, total
    def getNextValues(self, state, inp):
        (count, total) = state
        if count == 4:
            return ((count + 1, total + inp), total + inp)
        else:
            return ((count + 1, total + inp), None)
    def done(self, state):
        (count, total) = state
        # if count == 5, return True.
        return count == 5
    # While done is returning False, the state machines will keep running,
    # when it outputs True, it will stop.
c5 = ConsumeFiveValues()
print c5.transduce([5,10,7,8,12,18,20,50])
# I still don't know how to use the done method inside transduce to make it terminates.
# However, in the lib601, it is already done.

class Repeat(sm.SM):
    # Default value of n = None. If no values is inputed, it will repeat forever.
    def __init__(self, sm, n = None):
        # Receiving a machine.
        self.sm = sm
        # Updating the startState of Repeat.
        self.startState = (0, self.sm.startState) # number of times the constituent machine has been executed to completion, current state.
        # Number of times the machine should repeat its cycle.
        self.n = n
    def advanceIfDone(self, counter, smState): # counter is the number of times it has been repeated, smState is the state of the constituent machine
        # self.sm = c5 , self.done = Repeat
        # self.sm.sone(smState) = True when the constituent machine is done. self.done = False The whole cycle is not done yet.
        # While the constituent machine is done, but the repeat is not.
        while self.sm.done(smState) and not self.done((counter, smState)):
            # It counts the number of times it is repeating.
            counter = counter + 1
            # Restart the machine.
            smState = self.sm.startState
        # Then it returns the number of time the whole cycle has been repeated and the state of the constituent machine.
        return (counter, smState)
    def getNextValues(self, state, inp):
        # Getting the next state of the constituent machine.
        (counter, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        # Advance takes carry to see if the constituent machine has conclude it cycle and if the repeat has completed it cycle.
        # Then it return the counter updated and the state of the constituent machine updated.
        (counter, smState) = self.advanceIfDone(counter, smState)
        # Returning the nextstate of repeat and the output of repeat, which turns out to be the same of the constituent machine.
        return ((counter, smState), o)
    def done(self, state):
        # We know the whole Repeat is done if the counter is equal to n.
        # Receiving the number of times it has been repeated already. 
        (counter, smState) = state
        # It returns true if I already reached the number of times it should repeat.
        # If the default value is actioned it will never stop repeating.
        return counter == self.n

class CharTSM(sm.SM):
    startState = False
    def __init__(self, c):
        self.c = c
    def getNextValues(self, state, inp):
        return (True, self.c)
    def done(self, state):
        return state
# Easier to understand.
a = CharTSM('a')
print a.run(verbose = True)
a4 = sm.Repeat(a,4)
print a4.run()
# Same thing in just one line.
print sm.Repeat(CharTSM('a'),4).run()
# Repeating three times the ConsumeFiveValues.
print sm.Repeat(ConsumeFiveValues(), 3).transduce(range(100))


# Executes one machine until it is done and go to the next.
class Sequence(sm.SM):
    def __init__(self, smList):
        # List of the machines.
        self.smList = smList
        # How many machines were ran, the starting state of the first machine.
        self.startState = (0, self.smList[0].startState)
        # length of the list.(Quantity of machines)
        self.n = len(smList)  # 7
    
    def advanceIfDone(self, counter, smState):
        # If the constituent machine is done.
        while self.smList[counter].done(smState) and counter + 1 < self.n:
            # Go to the another.
            counter = counter + 1
            smState = self.smList[counter].startState
        return (counter, smState)
    def getNextValues(self, state, inp):
        # Separating what is in the state.
        (counter, smState) = state
        # Getting the nextstate and the output.
        (smState, o) = self.smList[counter].getNextValues(smState, inp)
        # See if it is complete
        (counter, smState) = self.advanceIfDone(counter, smState)
        # Retung the nextstate and the output.
        return ((counter, smState), o)
    def done(self, state):
        (counter, smState) = state
        return self.smList[counter].done(smState)

print sm.Sequence([CharTSM('a'), CharTSM('b'), CharTSM('c')]).run(verbose = True)
# The two following machines bellow execute the same output.
print sm.Sequence([ConsumeFiveValues(), ConsumeFiveValues(), ConsumeFiveValues()]).transduce(range(100))
print sm.Repeat(ConsumeFiveValues(), 3).transduce(range(100))

def makeTextSequence(str):
    return sm.Sequence([CharTSM(c) for c in str])
print makeTextSequence('Hello World').run(20, verbose = True)
print sm.Repeat(makeTextSequence('abc'), 3).run(verbose = True)

# 4.3.3 - RepeatUntil and Until

class RepeatUntil(sm.SM):
    def __init__(self, condition, sm):
        self.sm = sm
        sef.condition = condition
        self.startState = (False, self.sm.startState)
    def getNextValues(self, state, inp):
        (condTrue, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        # self.condition is a function and is receiving the input to check if the condition was already attended.
        condTrue = self.condition(inp)
        # If the constituent machine is done, but not the whole RepeatUntil.
        if self.sm.done(smState) and not condTrue:
            # Reset the machine.
            smState = self.sm.getStartState()
        return ((condTrue, smState), o)
    def done(self, state):
        (condTrue, smState) = state
        return self.sm.done(smState) and condTrue

# Executes until both the condition is true and the machine is terminated.
RU = sm.RepeatUntil(lambda x: x > 10, ConsumeFiveValues())
print RU.transduce(range(20), verbose = True)

# Until: Executes until either of the condition is True.

# Executes until the constituent machine is done, because the condition is never attended first.
U = sm.Until(lambda x: x > 10, ConsumeFiveValues())
print U.transduce(range(20), verbose = True)

# Executes until the condition is True. Do no terminate the constituent machine.
U2 = sm.Until(lambda x: x==2, ConsumeFiveValues())
print U2.transduce(range(20), verbose = True)

# As I didn't state how many times Repeat should be execute, it will never become done.
# Therefore the only thing which will make the machine stop running is the condition. (inp > 10)
m = sm.Until(lambda x: x > 10, sm.Repeat(ConsumeFiveValues()))
print m.transduce(range(20), verbose = True)
