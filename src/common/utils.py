"""
This file contains common utils for DryVR
"""

import importlib
import random

from collections import namedtuple


# This is the tuple for input file parsed from DryVR
DryVRInput = namedtuple(
	'DryVRInput',
	'vertex edge transtime variables initialSet unsafeSet timeHorizon path'
)

def importSimFunction(path):
	# Import simulation function from examples directory
	# Note the folder in the examples directory must have __init__
	# And the simulation function must be named TC_Simulate
	# This is beacuse we treat example as a python package
	path = path.replace('/', '.')
	module = importlib.import_module(path)
	return module.TC_Simulate

def randomPoint(lower, upper):
	# Pick a random Point between lower and upper bound
	# This function supports both int or list
	if isinstance(lower, int) or isinstance(lower, float):
		return random.uniform(lower, upper)

	if isinstance(lower, list):
		assert len(lower) == len(upper), "Random Point List Range Error"

		return [random.uniform(lower[i], upper[i]) for i in range(len(lower))]

def calcDelta(lower, upper):
	# Calculate the delta value between the lower and upper bound
	# The function only supports list since we assue initial set is always list
	assert len(lower) == len(upper), "Delta calc List Range Error"
	return [(upper[i]-lower[i])/2 for i in range(len(upper))]

def centerPoint(lower, upper):
	# Calculate the center point between the lower and upper bound
	# The function only supports list since we assue initial set is always list
	assert len(lower) == len(upper), "Center Point List Range Error"
	return [(upper[i]+lower[i])/2 for i in range(len(upper))]