"""
This file contains common utils for DryVR
"""

import importlib
import random

from collections import namedtuple


# This is the tuple for input file parsed by DryVR
DryVRInput = namedtuple(
    'DryVRInput',
    'vertex edge guards variables initialSet unsafeSet timeHorizon path resets initialMode deterministic bloatingMethod kvalue'
)

# This is the tuple for rtt input file parsed by DryVR
RrtInput = namedtuple(
    'RttInput',
    'modes initialMode variables initialSet unsafeSet goalSet timeHorizon minTimeThres path goal bloatingMethod kvalue'
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

    # Convert list into float in case they are int
    lower = [float(val) for val in lower]
    upper = [float(val) for val in upper]

    assert len(lower) == len(upper), "Delta calc List Range Error"
    return [(upper[i]-lower[i])/2 for i in range(len(upper))]

def calcCenterPoint(lower, upper):
    # Calculate the center point between the lower and upper bound
    # The function only supports list since we assue initial set is always list
    assert len(lower) == len(upper), "Center Point List Range Error"
    return [(upper[i]+lower[i])/2 for i in range(len(upper))]

def buildModeStr(g, vertex):
    # Build a unique string to represent a mode
    # This should be something like "modeName,modeNum"
    return g.vs[vertex]['label']+','+str(vertex)

def handleReplace(unsafe, keys):
    idxes = []
    i = 0
    original = unsafe

    keys.sort(key=lambda s:len(s))
    for key in keys[::-1]:
        for i in range(len(unsafe)):
            if unsafe[i:].startswith(key):
                idxes.append((i, i+len(key)))
                unsafe = unsafe[:i] + "@"*len(key) + unsafe[i+len(key):]

    idxes = sorted(idxes)

    unsafe = original
    for idx in idxes[::-1]:
        key = unsafe[idx[0]:idx[1]]
        target = 'self.varDic["'+key+'"]'
        unsafe = unsafe[:idx[0]] + target + unsafe[idx[1]:]
    return unsafe
