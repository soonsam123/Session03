import lib601.sm as sm
class ConsumeFiveValues(sm.SM):
    startState = (0,0)   # count, total
    def getNextValues(self, state, inp):
        (count, total) = state
        if count == 2:
            return ((count + 1, total + inp), total + inp)
        else:
            return ((count + 1, total + inp), None)
    def done(self, state):
        # If this method outputs false, the machine will stope running.
        (count, total) = state
        return count == 3
c5 = ConsumeFiveValues()
print c5.transduce([10,20,54,67,90,98,100,200])

class Repeat(sm.SM):
    def __init__(self, sm, n = None):
        self.sm = sm
        self.n = n
        # The state is the number of times the cycle has been repeated, and the state of the constituent machine.
        self.startState = (0, self.sm.startState)
    def AdvanceIfDone(self, counter, smState):
        # When the machine has completed it cycle, but the repeat has not.
        while self.sm.done(smState) and not self.done((counter, smState)):
            counter = counter + 1
            smState = self.sm.startState
        return (counter, smState)
    def getNextValues(self, state, inp):
        (counter, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        (counter, smState) = self.AdvanceIfDone(counter, smState)
        return ((counter, smState), o)
    def done(self, state):
        (counter, smState) = state
        return counter == self.n
    
fourTimes = Repeat(c5, 4)
print fourTimes.transduce([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
