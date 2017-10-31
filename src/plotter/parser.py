"""
This file consist parser code for DryVR reachtube output
"""

from linkednode import LinkedNode

def parse(data):
	
	initNode = None
	prevNode = None
	curNode = None
	lowerBound = {}
	upperBound = {}
	y_min = [float("inf") for _ in range(len(data[2].strip().split()))]
	y_max = [float("-inf") for _ in range(len(data[2].strip().split()))]

	for line in data:
		# This is a mode indicator
		if ',' in line or '->' in line or line.strip().isalpha():
			insertData(curNode, lowerBound, upperBound)
			# There is new a transition
			if '->' in line:
				modeList = line.strip().split('->')
				prevNode = initNode
				for i in range(1, len(modeList)-1):
					prevNode = prevNode.child[modeList[i]]
				curNode = prevNode.child.setdefault(modeList[-1], LinkedNode(modeList[-1], line))
			else:
				curNode = LinkedNode(line.strip(), line)
				initNode = curNode
			# Using dictionary becasue we want to concat data
			lowerBound = {}
			upperBound = {}
			LOWER = True

		else:
			line = map(float,line.strip().split())
			if LOWER:
				LOWER = False
				# This data appered in lowerBound before, concat the data
				if line[0] in lowerBound:
					for i in range(1,len(line)):
						lowerBound[line[0]][i] = min(lowerBound[line[0]][i], line[i])
				else:
					lowerBound[line[0]] = line

				for i in range(len(line)):
					y_min[i] = min(y_min[i], line[i])
			else:
				LOWER = True
				if line[0] in upperBound:
					for i in range(1,len(line)):
						upperBound[line[0]][i] = max(upperBound[line[0]][i], line[i])
				else:
					upperBound[line[0]] = line

				for i in range(len(line)):
					y_max[i] = max(y_max[i], line[i])
	insertData(curNode, lowerBound, upperBound)
	return initNode, y_min, y_max



def insertData(node, lowerBound, upperBound):
	if not node or len(lowerBound) == 0:
		return

	for key in lowerBound:
		if key in node.lowerBound:
			for i in range(1,len(lowerBound[key])):
				node.lowerBound[key][i] = min(node.lowerBound[key][i], lowerBound[key][i])
		else:	
			node.lowerBound[key] = lowerBound[key]

	for key in sorted(upperBound):
		if key in node.upperBound:
			for i in range(1,len(upperBound[key])):
				node.upperBound[key][i] = max(node.upperBound[key][i], upperBound[key][i])
		else:
			node.upperBound[key] = upperBound[key]