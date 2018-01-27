"""
This file contains uniform checker class for DryVR
"""
import sympy

from src.common.utils import handleReplace
from z3 import *


class UniformChecker():
	def __init__(self, unsafe, variables):
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
			self.solverDic[mode][1].add(eval(self._neg(cond)))

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



	def _neg(self, orig):
		# Neg the original condition
		return 'Not('+orig+')'

	def checkSimuTube(self, tube, mode):
		# Check the simulation trace result
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][0]
			symbols = self.solverDic[mode][2]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]
			symbols = self.solverDic['Allmode'][2]
		else:
			# Return True if we do not check this mode
			return 1

		for t in tube:
			curSolver.push()
			for symbol in symbols:
				curSolver.add(self.varDic[symbol] == t[symbols[symbol]])
			# curSolver.add(self.varDic['t'] == t[0])
			# for i in range(1, len(t)):
			# 	if self.variables[i-1] in symbols:
			# 		curSolver.add(self.varDic[self.variables[i-1]]==t[i])

			if curSolver.check() == sat:
				curSolver.pop()
				return -1
			else:
				curSolver.pop()
		return 1

	def checkReachTube(self, tube, mode):
		# Check the reach tube result
		if not mode in self.solverDic and not 'Allmode' in self.solverDic:
			# Return True if we do not check this mode
			return 1

		safe = 1
		for i in range(0, len(tube), 2):
			lower = tube[i]
			upper = tube[i+1]
			if self._checkIntersection(lower, upper, mode):
				if self._checkContainment(lower, upper, mode):
					# The unsafe region is fully contained
					return -1
				else:
					# We do not know if it is truly unsafe or not
					safe = 0
		return safe

	def cutTubeTillUnsafe(self, tube):
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
		# Check if the reach tube intersect with the unsafe region
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

		# curSolver.add(self.varDic["t"]>=lower[0])
		# curSolver.add(self.varDic["t"]<=upper[0])

		# for i in range (1,len(lower)):
		# 	if self.variables[i-1] in symbols:
		# 		curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
		# 		curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])

		if curSolver.check() == sat:
			curSolver.pop()
			return True
		else:
			curSolver.pop()
			return False

	def _checkContainment(self, lower, upper, mode):
		# Check if the reach tube is fully contained in unsafe region
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

		# curSolver.add(self.varDic["t"]>=lower[0])
		# curSolver.add(self.varDic["t"]<=upper[0])

		# for i in range (1,len(lower)):
		# 	if self.variables[i-1] in symbols:
		# 		curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
		# 		curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])

		if curSolver.check() == sat:
			curSolver.pop()
			return False
		else:
			curSolver.pop()
			return True
