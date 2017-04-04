import lib601.sm as sm

# This simple machine can manage an automatic soda seller.
# Adding more options would become an automatic complex machine.
# Actually it seems to be complex, but it is pretty easy to do when you know state machines.
class Vending(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        if inp == 'quarter':
            return (state + 25, (0, False))
        elif inp == 'cancel':
            return (0, (state, False))
        elif inp == 'dispense':
            if state < 75:
                return (0, (state, False))
            else:
                return (0, (state - 75, True))

print Vending().transduce(['dispense', 'quarter', 'quarter', 'quarter', 'quarter', 'dispense', 'quarter', 'cancel', 'dispense'])
