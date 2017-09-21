'''
This is a data structure to hold reachtube data per node
'''
class LinkedNode():
	def __init__(self, nodeId, fileName):
		self.fileName = fileName.strip()
		self.nodeId = nodeId
		self.lowerBound = {}
		self.upperBound = {}
		self.child = {}
