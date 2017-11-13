from sympy.solvers import solve
from sympy import Symbol
import sympy

rawequ = "x=0.8*x"
#rawequ = "x=3.5"

variableList = ['x', 'y', 'z', 'w']
lowerBound = [1.0,2.0,3.0,4.0]
upperBound = [2.0,3.0,4.0,5.0]

# Parse the equ
equ_split = rawequ.split('=')
lhs, rhs = equ_split[0], equ_split[1]
target = sympy.sympify(lhs)
equ = sympy.Eq(sympy.sympify(lhs) - sympy.sympify(rhs), 0 )
newequ = sympy.sympify(rhs)
print newequ
# # Find out what variable is used
symbols = list(sympy.sympify(rhs).free_symbols) # set
# print symbols

def buildAllCombo(symbols, variableList, lowerBound, upperBound):
    if not symbols:
    	return []

    curSymbol = str(symbols[0])
    idx = variableList.index(curSymbol)
    lo = lowerBound[idx]
    up = upperBound[idx]
    ret = []
    nextLevel = buildAllCombo(symbols[1:], variableList, lowerBound, upperBound)
    if nextLevel:
        for n in nextLevel:
            ret.append(n+[(symbols[0], lo)])
            ret.append(n+[(symbols[0], up)])
    else:
        ret.append([(symbols[0], lo)])
        ret.append([(symbols[0], up)])
    return ret

combos = buildAllCombo(symbols, variableList, lowerBound, upperBound)
# finalEqu = solve(equ,target)[0]
# print finalEqu

minReset = float("inf")
maxReset = float("-inf")

if combos:
    for combo in combos:
        result = float(newequ.subs(combo))
        minReset = min(minReset, float(result))
        maxReset = max(maxReset, float(result))
else:
    minReset = float(newequ)
    maxReset = float(newequ)

print "max value of", str(target), "after reset is", maxReset
print "min value of", str(target), "after reset is", minReset
