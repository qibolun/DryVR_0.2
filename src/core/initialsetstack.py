"""
This file contains initial set class stack for DryVR
"""
import random

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

	def __str__(self):
		# Build string representation for the initial set
		ret = "===============================================\n"
		ret += "Mode: "+str(self.mode)+"\n"
		ret += "stack size: "+str(len(self.stack))+"\n"
		ret += "remainTime: "+str(self.remainTime)+"\n"
		return ret


class RrtSetStack():
	def __init__(self, mode, remainTime, minTimeThres, level):
		self.mode = mode
		self.parent = None
		self.initial = None
		self.bloatedTube = []
		self.remainTime = remainTime
		self.minTimeThres = minTimeThres
		self.children = {}
		self.visited = set()
		self.candidates = []
		self.level = level

	def randomPicker(self, k):
		# random pick k points from tube
		i = 0
		ret = []
		while i < len(self.bloatedTube):
			if self.bloatedTube[i][0] >= self.minTimeThres:
				ret.append((self.bloatedTube[i], self.bloatedTube[i+1]))
			i+=2

		random.shuffle(ret)
		return ret[:k]

	def __str__(self):
		# Build string representation for the initial set
		ret = ""
		ret += "Level: "+str(self.level)+"\n"
		ret += "Mode: "+str(self.mode)+"\n"
		ret += "Initial: "+str(self.initial)+"\n"
		ret += "visited: "+str(self.visited)+"\n"
		ret += "num candidates: "+str(len(self.candidates))+"\n"
		if self.bloatedTube:
			ret += "bloatedTube: True"+"\n"
		else:
			ret += "bloatedTube: False"+"\n"
		return ret
