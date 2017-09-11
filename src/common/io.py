"""
This file contains IO functions for DryVR
"""

import json

from utils import DryVRInput

def writeToFile(result, path):
	# Write result to file
	with open(path, 'w') as f:
		for interval in result:
			f.write(' '.join(map(str,interval))+'\n')

def readFromFile(path):
	# Read result from file
	trace = []
	with open(path, 'r') as f:
		for line in f:
			trace.append([float(x) for x in line.split()])
	return trace

def writeReachTubeFile(result, path):
	# Write reach tube result
	with open(path, 'w') as f:
		for line in result:
			if isinstance(line, str):
				f.write(line+'\n')
			elif isinstance(line, list):
				f.write(' '.join(map(str,line))+'\n')

def parseInputFile(path):
	# Parse the input file for DryVR
	with open(path, 'r') as f:
		data = json.load(f)
		
		return DryVRInput(
			vertex=data["vertex"],
			edge=data["edge"],
			guards=data["guards"],
			variables=data["variables"],
			initialSet=data["initialSet"],
			unsafeSet=data["unsafeSet"],
			timeHorizon=data["timeHorizon"],
			path=data["directory"],
		)