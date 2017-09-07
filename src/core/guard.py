"""
This file contains initial set class for DryVR
"""

import random

from z3 import *

class Guard():
	def __init__(self, variables):
		self.varDic = {'t':Real('t')}
		self.variables = variables
		for var in variables:
			self.varDic[var] = Real(var)

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

	def _buildGuard(self, guardStr):
		# Build solver for current guard based on guard string
		curSolver = Solver()
		for key in sorted(self.varDic)[::-1]:
			# Replace the variable to self.vardic + variable
			guardStr = self._replace(guardStr,key)
		curSolver.add(eval(guardStr))
		return curSolver

	def guardSimuTube(self, tube, guardStr):
		if not guardStr:
			return None, tube

		curSolver = self._buildGuard(guardStr)
		guardSet = {}
		for idx,t in enumerate(tube):
			curSolver.push()
			curSolver.add(self.varDic['t'] == t[0])
			for i in range(1, len(t)):
				curSolver.add(self.varDic[self.variables[i-1]]==t[i])

			if curSolver.check() == sat:
				# The simulation trace hits the guard
				curSolver.pop()
				guardSet[idx] = t
			else:
				curSolver.pop()
				if guardSet:
					# Guard is not empty, randomly pick one and return
					idx, point = random.choice(list(guardSet.items()))
					# Return the initial point for next mode, and truncked tube
					return point[1:], tube[:idx+1]

		# No guard hits for current tube
		return None, tube


