# Name: Soon Sam R Santos
# Date: March 10, 2017
# Session: 3
# Aditional_Questions.py

#***********WK.3.3.1 - Map**************
# Part 1
print "*************WK.3.3.1"
print "*************Part 1"
def sq(x): return x*x
def mapList(function, list):
    return [function(i) for i in list]
# TestCases
print mapList(sq, [1,2,3,4])
print "------------------------------------------------" # Organazing
# Part 2
print "*************Part 2"
def sumAbs(list_num):
    return sum([abs(i) for i in list_num])
# TestCases
print sumAbs(mapList(sq, [1,2,3,4]))
print "------------------------------------------------" # Organazing
# Part 3
print "*************Part 3"
def diff(x, y): return x - y
def mapSquare(function, list):
    return [[diff(x, y) for x in list] for y in list]
print mapSquare(diff, [1,2,3])
print "------------------------------------------------" # Organazing
# **********WK.3.3.2 - Indexing Nest Lists*************
print "*************WK.3.3.2"
nested = [[[1,2],3],[4,[5,6]],7,[8,9,10]]
print nested[3][1], nested[1][1][0]
def recursiveRef(nested_list, list_index):
    i = 0
    # BaseCase.
    if len(list_index) == 0:
        return nested_list
    return recursiveRef(nested_list, list_index[i])
print recursiveRef(nested, [])
print recursiveRef(nested, [3,1])
print recursiveRef(nested, [1,1,0])
print recursiveRef(nested, [1,1])

# **********WK.3.3.2 - Indexing Nest Lists*************
