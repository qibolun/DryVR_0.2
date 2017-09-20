"""
This file contains initial set class stack for DryVR
"""

class InitialSetStack():
	def __init__(self, mode, threshold, remainTime):
		self.mode = mode
		self.threshold = threshold
		self.parent = None
		self.stack = []
		self.remainTime = remainTime
		self.bloatedTube = []

	def isValid(self):
		# Check if number of element in stack is more than threshold
		return len(self.stack) <= self.threshold