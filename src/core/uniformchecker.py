"""
This file contains uniform checker class for DryVR
"""
import sympy

from src.common.constant import *
from src.common.utils import handleReplace, neg
from z3 import *


class UniformChecker():
	"""
    This is class for check unsafe checking
    """
	def __init__(self, unsafe, variables):
		"""
		Reset class initialization function.

        Args:
        	unsafe (str): unsafe constraint
            variables (list): list of varibale name
        """
		self.varDic = {'t':Real('t')}
		self.variables = variables
		self.solverDic = {}
		for var in variables:
			self.varDic[var] = Real(var)

		if not unsafe:
			return

		original = unsafe

		unsafe = handleReplace(unsafe, self.varDic.keys())
		unsafeList = unsafe[1:].split('@')
		for unsafe in unsafeList:
			mode, cond = unsafe.split(':')
			self.solverDic[mode] = [Solver(), Solver()]
			self.solverDic[mode][0].add(eval(cond))
			self.solverDic[mode][1].add(eval(neg(cond)))

		unsafeList = original[1:].split('@')
		for unsafe in unsafeList:
			mode, cond = unsafe.split(':')
			# This magic line here is because sympy will evaluate == to be False
			# Therefore we are not be able to get free symbols from it
			# Thus we need to replace "==" to something else, which is >=
			cond = cond.replace("==",">=")
			symbols = list(sympy.sympify(cond).free_symbols)
			symbols = [str(s) for s in symbols]
			symbolsIdx = {s:self.variables.index(s)+1 for s in symbols if s in self.variables}
			if 't' in symbols:
				symbolsIdx['t'] = 0
			self.solverDic[mode].append(symbolsIdx)

	def checkSimuTrace(self, traces, mode):
		"""
		Check the simulation trace

        Args:
            traces (list): simulation traces
            mode (str): mode need to be checked

        Returns:
            An int for checking result SAFE = 1, UNSAFE = -1
        """
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][0]
			symbols = self.solverDic[mode][2]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]
			symbols = self.solverDic['Allmode'][2]
		else:
			# Return True if we do not check this mode
			return SAFE

		for t in traces:
			curSolver.push()
			for symbol in symbols:
				curSolver.add(self.varDic[symbol] == t[symbols[symbol]])

			if curSolver.check() == sat:
				curSolver.pop()
				return UNSAFE
			else:
				curSolver.pop()
		return SAFE

	def checkReachTube(self, tube, mode):
		"""
		Check the bloated reach tube

        Args:
            tube (list): reach tube
            mode (str): mode need to be checked

        Returns:
            An int for checking result SAFE = 1, UNSAFE = -1, UNKNOWN = 0
        """
		if not mode in self.solverDic and not 'Allmode' in self.solverDic:
			# Return True if we do not check this mode
			return SAFE

		safe = SAFE
		for i in range(0, len(tube), 2):
			lower = tube[i]
			upper = tube[i+1]
			if self._checkIntersection(lower, upper, mode):
				if self._checkContainment(lower, upper, mode):
					# The unsafe region is fully contained
					return UNSAFE
				else:
					# We do not know if it is truly unsafe or not
					safe = UNKNOWN
		return safe

	def cutTubeTillUnsafe(self, tube):
		"""
		Truncated the tube before it intersect with unsafe set

        Args:
            tube (list): reach tube

        Returns:
            truncated tube
        """
		if not self.solverDic:
			return tube
		# Cut the reach tube till it intersect with unsafe
		for i in range(0, len(tube), 2):
			lower = tube[i]
			upper = tube[i+1]
			if self._checkIntersection(lower, upper, 'Allmode'):
				# we need to cut here
				return tube[:i]

		return tube


	def _checkIntersection(self, lower, upper, mode):
		"""
		Check if current set intersect with the unsafe set

        Args:
            lower (list): lowerbound of the current set
            upper (list): upperbound of the current set
            mode (str): the mode need to be checked

        Returns:
            Return a bool to indicate if the set intersect with the unsafe set
        """
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][0]
			symbols = self.solverDic[mode][2]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]
			symbols = self.solverDic['Allmode'][2]

		curSolver.push()
		for symbol in symbols:
			curSolver.add(self.varDic[symbol] >= lower[symbols[symbol]])
			curSolver.add(self.varDic[symbol] <= upper[symbols[symbol]])

		checkResult = curSolver.check()

		if checkResult == sat:
			curSolver.pop()
			return True
		if checkResult == unknown:
			print "Z3 return unknown result"
			exit()
		else:
			curSolver.pop()
			return False

	def _checkContainment(self, lower, upper, mode):
		"""
		Check if the current set is fully contained in unsafe region

        Args:
            lower (list): lowerbound of the current set
            upper (list): upperbound of the current set
            mode (str): the mode need to be checked

        Returns:
            Return a bool to indicate if the set is fully contained in unsafe region
        """
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][1]
			symbols = self.solverDic[mode][2]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][1]
			symbols = self.solverDic['Allmode'][2]

		curSolver.push()
		for symbol in symbols:
			curSolver.add(self.varDic[symbol] >= lower[symbols[symbol]])
			curSolver.add(self.varDic[symbol] <= upper[symbols[symbol]])
		checkResult = curSolver.check()

		if checkResult == sat:
			curSolver.pop()
			return False
		if checkResult == unknown:
			print "Z3 return unknown result"
			exit()
		else:
			curSolver.pop()
			return True
