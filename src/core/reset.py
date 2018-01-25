"""
This file contains reset class for DryVR
"""

import sympy

from sympy.solvers import solve
from src.common.utils import randomPoint

class Reset():
	def __init__(self, variables):
		self.variables = variables

	def resetReachTube(self, rawEqus, lowerBound, upperBound):
		if not rawEqus:
			return lowerBound, upperBound

		rawEqus = rawEqus.split(';')
		lbList = []
		ubList = []
		for rawEqu in rawEqus:
			lb, ub = self._handleReset(rawEqu, lowerBound, upperBound)
			lbList.append(lb)
			ubList.append(ub)

		return self._mergeResult(lbList, ubList, lowerBound, upperBound)


	def resetSimTrace(self, rawEqus, point):
		# Using reset Reachtube function to handle this case

		if point == [] or not point:
			return point
		lower, upper = self.resetReachTube(rawEqus, point, point)
		return randomPoint(lower, upper)

	def _mergeResult(self, lbList, ubList, lowerBound, upperBound):
		# Merge all reset value

		# Copy the list
		retLb = list(lowerBound)
		retUb = list(upperBound)

		for i in range(len(lbList)):
			curLb = lbList[i]
			curUb = ubList[i]
			for j in range(len(curLb)):
				if curLb[j]!=lowerBound[j]:
					retLb[j] = curLb[j]
				if curUb[j]!=upperBound[j]:
					retUb[j] = curUb[j]
		return retLb, retUb

	def _buildAllCombo(self, symbols, lowerBound, upperBound):
		# This function allows us to build all combination given vars in symbol
		if not symbols:
			return []

		curSymbol = str(symbols[0])
		idx = self.variables.index(curSymbol)
		lo = lowerBound[idx]
		up = upperBound[idx]
		ret = []
		nextLevel = self._buildAllCombo(symbols[1:], lowerBound, upperBound)
		if nextLevel:
			for n in nextLevel:
				ret.append(n+[(curSymbol, lo)])
				ret.append(n+[(curSymbol, up)])
		else:
			ret.append([curSymbol, lo])
			ret.append([curSymbol, up])
		return ret


	def _handleWrappedReset(self, rawEqu, lowerBound, upperBound):
		# This is a function to handle reset such as 
		# V = [0, V+1]
		finalEqu = sympy.sympify(rawEqu)
		rhsSymbols = list(finalEqu.free_symbols)
		combos = self._buildAllCombo(rhsSymbols, lowerBound, upperBound)
		minReset = float('inf')
		maxReset = float('-inf')
		if combos:
			for combo in combos:
				if len(combo) == 2:
					result = float(finalEqu.subs(combo[0], combo[1]))
				else:
					result = float(finalEqu.subs(combo))
				minReset = min(minReset, float(result))
				maxReset = max(maxReset, float(result))
		else:
			minReset = float(finalEqu)
			maxReset = float(finalEqu)
		return (minReset, maxReset)



	def _handleReset(self, rawEqu, lowerBound, upperBound):
		equSplit = rawEqu.split('=')
		lhs, rhs = equSplit[0], equSplit[1]
		target = sympy.sympify(lhs)
		# Construct the equation
		finalEqu = sympy.sympify(rhs)
		if not isinstance(finalEqu, list):
			rhsSymbols = list(sympy.sympify(rhs).free_symbols)
		else:
			rhsSymbols = None
		# print target, rhsSymbols
		combos = self._buildAllCombo(rhsSymbols, lowerBound, upperBound)
		# finalEqu = solve(equ, target)[0]

		minReset = float('inf')
		maxReset = float('-inf')
		if combos:
			for combo in combos:
				if len(combo) == 2:
					result = float(finalEqu.subs(combo[0], combo[1]))
				else:
					result = float(finalEqu.subs(combo))
				minReset = min(minReset, float(result))
				maxReset = max(maxReset, float(result))
		elif isinstance(finalEqu, list):
			minReset = min(self._handleWrappedReset(finalEqu[0], lowerBound, upperBound))
			maxReset = max(self._handleWrappedReset(finalEqu[1], lowerBound, upperBound))
		else:
			minReset = float(finalEqu)
			maxReset = float(finalEqu)

		retLb = list(lowerBound)
		retUb = list(upperBound)
		targetIdx = self.variables.index(str(target))
		retLb[targetIdx] = minReset
		retUb[targetIdx] = maxReset
		return retLb, retUb
