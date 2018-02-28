"""
This file contains a distance checker class for controller synthesis
"""
from math import sqrt
from z3 import *


class DistChecker():
	"""
	This is the class to calculate the distance between 
	current set and the goal set for DryVR controller synthesis.
	The distance it calculate is the euclidean distance.
    """
	def __init__(self, goalSet, variables):
		"""
		Distance checker class initialization function.

        Args:
            goalSet (list): a list describle the goal set.
            	[["x_1","x_2"],[19.5,-1],[20.5,1]]
            	which defines a goal set
            	19.5<=x_1<=20.5 && -1<=x_2<=1
            variables (list): list of varibale name
        """
		var, self.lower, self.upper = goalSet
		self.idx = []
		for v in var:
			self.idx.append(variables.index(v)+1)

	def calcDistance(self, lowerBound, upperBound):
		"""
		Calculate the euclidean distance between the
		current set and goal set.

        Args:
            lowerBound (list): the lower bound of the current set.
            upperBound (list): the upper bound of the current set.

        Returns:
            the euclidean distance between current set and goal set

        """
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

