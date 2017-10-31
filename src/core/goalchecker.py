"""
This file contains uniform checker class for DryVR
"""

from z3 import *

class GoalChecker():
	def __init__(self, goal, variables):
		self.varDic = {'t':Real('t')}
		self.variables = variables
		for var in variables:
			self.varDic[var] = Real(var)
		for key in sorted(self.varDic)[::-1]:
			# Replace the variable to self.vardic + variable
			goal = self._replace(goal,key)

		self.intersectChecker = Solver()
		self.containChecker = Solver()

		self.intersectChecker.add(eval(goal))
		self.containChecker.add(eval(self._neg(goal)))

	def _replace(self, unsafe, key):
		# Replace the key in the unsafe string to target
		target = 'self.varDic["'+key+'"]'
		idxes = []
		for i in range(len(unsafe)):
			if unsafe[i:].startswith(key):
				idxes.append(i)

		for idx in idxes[::-1]:
			if idx != 0 and unsafe[idx-1] == '"':
				continue
			unsafe = unsafe[:idx] + target + unsafe[idx+len(key):]
		return unsafe

	def _neg(self, orig):
		# Neg the original condition
		return 'Not('+orig+')'

	def goalSimuTube(self, tube):
		# Check the simulation trace result
		curSolver = self.intersectChecker

		for idx, t in enumerate(tube):
			curSolver.push()
			curSolver.add(self.varDic['t'] == t[0])
			for i in range(1, len(t)):
				curSolver.add(self.varDic[self.variables[i-1]]==t[i])

			if curSolver.check() == sat:
				curSolver.pop()
				return tube[:idx+1]
			else:
				curSolver.pop()
		return []

	def goalReachTube(self, tube):
		for i in range(0, len(tube), 2):
			lower = tube[i]
			upper = tube[i+1]
			if self._checkIntersection(lower, upper):
				if self._checkContainment(lower, upper):
					return True, tube[:i+2]
		return False, tube

	def _checkIntersection(self, lower, upper):
		curSolver = self.intersectChecker
		curSolver.push()
		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])
		for i in range(1, len(lower)):
			curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
			curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])
		if curSolver.check() == sat:
			curSolver.pop()
			return True
		else:
			curSolver.pop()
			return False

	def _checkContainment(self, lower, upper):
		curSolver = self.containChecker
		curSolver.push()
		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])
		for i in range(1, len(lower)):
			curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
			curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])
		if curSolver.check() == sat:
			curSolver.pop()
			return False
		else:
			curSolver.pop()
			return True

