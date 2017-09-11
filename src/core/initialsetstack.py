"""
This file contains initial set class stack for DryVR
"""

def InitialSetStack():
	def __init__(self, mode, threshold):
		self.mode = mode
		self.threshold = threshold
		self.parent = {}
		self.child = {}
		self.stack = []

	def isValid(self):
		# Check if number of element in stack is more than threshold
		return len(self.stack) < self.threshold