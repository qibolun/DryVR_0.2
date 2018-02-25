"""
This file contains reset class for DryVR
"""

import sympy

from sympy.solvers import solve
from src.common.utils import randomPoint

class Reset():
	"""
    This is class for resetting the initial set
    """
	def __init__(self, variables):
		"""
		Reset class initialization function.

        Args:
            variables (list): list of varibale name
        """
		self.variables = variables

	def resetSet(self, rawEqus, lowerBound, upperBound):
		"""
		Reset the initial set based on reset expressions

        Args:
            rawEqus (list): list of reset expression
            lowerBound (list): lower bound of the initial set
            upperBound (list): upper bound of the initial set

        Returns:
            lower bound and upper bound of the initial set after reset
        """
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


	def resetPoint(self, rawEqus, point):
		"""
		Reset the initial point based on reset expressions

        Args:
            rawEqus (list): list of reset expression
            point (list): the initial point need to be reset

        Returns:
            a point after reset
        """
		if point == [] or not point:
			return point
		lower, upper = self.resetSet(rawEqus, point, point)
		return randomPoint(lower, upper)

	def _mergeResult(self, lbList, ubList, lowerBound, upperBound):
		"""
		Merge the a list of reset result
		Since we allow multiple reset per transition,
		we get list of reset result, each result corresponding to one reset expression
		We need to merge all reset result together

        Args:
            lbList (list): list of reset lowerbound results
            ubList (list): list of reset upperbound results
            lowerBound(list): original lowerbound
			upperBound(list): original upperbound

        Returns:
            Upperbound and lowerbound after merge the reset result
        """
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
		"""
		This function allows us to build all combination given symbols
		For example, if we have a 2-dimension set for dim A and B.
		symbols = [A,B]
		lowerBound = [1.0, 2.0]
		upperBound = [3.0, 4.0]
		Then the result shold be all possible combination of the value of A and B
		result:
			[[1.0, 2.0], [3.0, 4.0], [3.0, 2.0], [1.0, 4.0]] 

        Args:
            symbols (list): symbols we use to create combo
            lowerBound (list): lowerbound of the set
			upperBound (list): upperbound of the set

        Returns:
            List of combination value
        """
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
		"""
		This is a function to handle reset such as V = [0, V+1]

        Args:
            rawEqu (str): reset equation
            lowerBound (list): lowerbound of the set
			upperBound (list): upperbound of the set

        Returns:
            Upperbound and lowerbound after the reset
        """
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
		"""
		Handle the reset with single reset expression

        Args:
            rawEqu (str): reset equation
            lowerBound (list): lowerbound of the set
			upperBound (list): upperbound of the set

        Returns:
            Upperbound and lowerbound after the reset
        """
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
