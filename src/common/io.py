"""
This file contains IO functions for DryVR
"""

import json

from utils import DryVRInput, RrtInput

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
			if isinstance(line, unicode):
				f.write(line+'\n')
			elif isinstance(line, list):
				f.write(' '.join(map(str,line))+'\n')

def writeRrtResultFile(modes, traces, path):
	with open(path, 'w') as f:
		for mode, trace in zip(modes, traces):
			f.write(mode + '\n')
			for line in trace:
				f.write(" ".join(map(str, line))+'\n')

def logEvent(logStr, path):
	pass


def parseInputFile(path):
	# Parse the input file for DryVR
	with open(path, 'r') as f:
		data = json.load(f)

		# If resets is missing, fill with empty resets
		if not 'resets' in data:
			data['resets'] = ["" for _ in range(len(data["edge"]))]

		# If initialMode is missing, fill with empty initial mode
		if not 'initialMode' in data:
			data['initialMode'] = ""

		# If deterministic is missing, defaultdict to non-deterministic
		if not 'deterministic' in data:
			data['deterministic'] = False

		return DryVRInput(
			vertex=data["vertex"],
			edge=data["edge"],
			guards=data["guards"],
			variables=data["variables"],
			initialSet=data["initialSet"],
			unsafeSet=data["unsafeSet"],
			timeHorizon=data["timeHorizon"],
			path=data["directory"],
			resets=data["resets"],
			initialMode=data["initialMode"],
			deterministic=data["deterministic"],
		)

def parseRrtInputFile(path):
	# Parse the rtt file for DryVR
	with open(path, 'r') as f:
		data = json.load(f)

		return RrtInput(
			modes = data["modes"],
			initialMode = data["initialMode"],
			variables = data["variables"],
			initialSet = data["initialSet"],
			unsafeSet = data["unsafeSet"],
			goalSet = data["goalSet"],
			timeHorizon = data["timeHorizon"],
			minTimeThres = data["minTimeThres"],
			path = data["directory"],
			goal = data["goal"],
		)
