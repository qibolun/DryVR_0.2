# A class handles distance calculation for RTT example

from math import sqrt
from z3 import *


class DistChecker():
	def __init__(self, distStr, variables):
		var, self.lower, self.upper = distStr
		self.idx = []
		for v in var:
			self.idx.append(variables.index(v)+1)

	def calcDistance(self, lowerBound, upperBound):
		dist = 0.0
		for i in range(len(self.idx)):
			maxVal = max(
				(self.lower[i]-lowerBound[self.idx[i]])**2,
				(self.upper[i]-lowerBound[self.idx[i]])**2,
				(self.lower[i]-upperBound[self.idx[i]])**2,
				(self.upper[i]-upperBound[self.idx[i]])**2
			)
			dist+=maxVal
		return sqrt(dist)

