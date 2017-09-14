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
			# Replace the variable to self.varDic + variable
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
					# Guard set is not empty, randomly pick one and return
					idx, point = random.choice(list(guardSet.items()))
					# Return the initial point for next mode, and truncked tube
					return point[1:], tube[:idx+1]

		# No guard hits for current tube
		return None, tube

	def guardReachTube(self, tube, guardStr):
		if not guardStr:
			return None, tube

		curSolver = self._buildGuard(guardStr)
		guardSetLower = []
		guardSetUpper = []
		for i in range(0,len(tube),2):
			curSolver.push()
			lowerBound = tube[i]
			upperBound = tube[i+1]
			curSolver.add(self.varDic['t'] >= lowerBound[0])
			curSolver.add(self.varDic['t'] <= upperBound[0])
			for j in range(1,len(lowerBound)):
				curSolver.add(self.varDic[self.variables[j-1]]>=lowerBound[j])
				curSolver.add(self.varDic[self.variables[j-1]]<=upperBound[j])

			if curSolver.check() == sat:
				# The reachtube hits the guard
				curSolver.pop()
				guardSetLower.append(lowerBound)
				guardSetUpper.append(upperBound)
			else:
				curSolver.pop()
				if guardSetLower:
					# Guard set is not empty, build the next initial set and return
					# At some point we might futher reduce the initial set for next mode
					initLower = guardSetLower[0][1:]
					initUpper = guardSetUpper[0][1:]
					for j in range(1,len(guardSetLower)):
						for k in range(1,len(guardSetLower[0])):
							initLower[k-1] = min(initLower[k-1], guardSetLower[j][k])
							initUpper[k-1] = max(initUpper[k-1], guardSetUpper[j][k])
					# Return next initial Set, the result tube, and the true transit time
					return [initLower,initUpper], tube[:i], guardSetLower[0][0]
		return None, tube, tube[-1][0]
