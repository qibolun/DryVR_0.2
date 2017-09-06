"""
This file contains initial set class for DryVR
"""

class InitialSet():
	def __init__(self, lower, upper):
		self.upperBound = upper
		self.lowerBound = lower
		self.delta = [(upper[i]-lower[i])/2.0 for i in range(len(upper))]
	
	def refine(self):
		# Refine the initial set into two smaller set
		# based on index with largest delta
		idx = self.delta.index(max(self.delta))
		# Construct first smaller initial set
		initSetOneUB = self.upperBound
		initSetOneLB = self.lowerBound
		initSetOneLB[idx] += self.delta[idx]
		# Construct second smaller initial set
		initSetTwoUB = self.upperBound
		initSetTwoLB = self.lowerBound
		initSetTwoUB[idx] -= self.delta[idx]

		return (
			InitialSet(initSetOneLB,initSetOneUB),
			InitialSet(initSetTwoLB,initSetTwoUB),
		)

	def __str__(self):
		# Build string representation for the initial set
		ret = ""
		ret += "Lower Bound: "+str(self.lowerBound)+"\n"
		ret += "Upper Bound: "+str(self.upperBound)+"\n"
		ret += "Delta: "+str(self.delta)+"\n"
		return ret 
