"""
This file contains uniform checker class for DryVR
"""

from src.common.utils import handleReplace
from z3 import *


class UniformChecker():
	def __init__(self, unsafe, variables):
		self.varDic = {'t':Real('t')}
		self.variables = variables
		self.solverDic = {}
		for var in variables:
			self.varDic[var] = Real(var)
		unsafe = handleReplace(unsafe, self.varDic.keys())
		unsafeList = unsafe[1:].split('@')
		for unsafe in unsafeList:
			mode, cond = unsafe.split(':')
			self.solverDic[mode] = [Solver(), Solver()]
			self.solverDic[mode][0].add(eval(cond))
			self.solverDic[mode][1].add(eval(self._neg(cond)))

	def _neg(self, orig):
		# Neg the original condition
		return 'Not('+orig+')'

	def checkSimuTube(self, tube, mode):
		# Check the simulation trace result
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][0]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]
		else:
			# Return True if we do not check this mode
			return 1

		for t in tube:
			curSolver.push()
			curSolver.add(self.varDic['t'] == t[0])
			for i in range(1, len(t)):
				curSolver.add(self.varDic[self.variables[i-1]]==t[i])

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
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]

		curSolver.push()

		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])

		for i in range (1,len(lower)):
			curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
			curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])

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
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][1]

		curSolver.push()

		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])

		for i in range (1,len(lower)):
			curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
			curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])

		if curSolver.check() == sat:
			curSolver.pop()
			return False
		else:
			curSolver.pop()
			return True
