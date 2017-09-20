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

	for line in data:
		# This is a mode indicator
		if ',' in line:
			insertData(curNode, lowerBound, upperBound)
			# There is new a transition
			if '->' in line:
				modeList = line.strip().split('->')
				prevNode = initNode
				for i in range(1, len(modeList)-1):
					prevNode = prevNode.child[modeList[i]]
				prevNode.child[modeList[-1]] = LinkedNode(modeList[-1])
				curNode = prevNode.child[modeList[-1]]
			else:
				curNode = LinkedNode(line.strip())
				initNode = curNode
			# Using dictionary becasue we want to concat data
			lowerBound = {}
			upperBound = {}
			LOWER = True

		else:
			line = line.strip().split()
			if LOWER:
				LOWER = False
				# This data appered in lowerBound before, concat the data
				if line[0] in lowerBound:
					for i in range(1,len(line)):
						lowerBound[line[0]][i] = min(lowerBound[line[0]][i], line[i])
				else:
					lowerBound[line[0]] = line
			else:
				LOWER = True
				if line[0] in upperBound:
					for i in range(1,len(line)):
						upperBound[line[0]][i] = max(upperBound[line[0]][i], line[i])
				else:
					upperBound[line[0]] = line
	return initNode



def insertData(node, lowerBound, upperBound):
	if not node or len(lowerBound) == 0:
		return

	for key in sorted(lowerBound):
		node.lowerBound.append(lowerBound[key])

	for key in sorted(upperBound):
		node.upperBound.append(upperBound[key])