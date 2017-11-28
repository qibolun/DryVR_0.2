"""
This file contains common utils for DryVR
"""

import importlib
import random

from collections import namedtuple


# This is the tuple for input file parsed by DryVR
DryVRInput = namedtuple(
    'DryVRInput',
    'vertex edge guards variables initialSet unsafeSet timeHorizon path resets initialMode deterministic'
)

# This is the tuple for rtt input file parsed by DryVR
RrtInput = namedtuple(
    'RttInput',
    'modes initialMode variables initialSet unsafeSet goalSet timeHorizon minTimeThres path goal'
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

    while i < len(unsafe):
        tempStr = ''
        while unsafe[i].isalpha():
            tempStr += unsafe[i]
            i+=1
        if tempStr in keys:
            idxes.append((i-len(tempStr), i))
            continue
        elif tempStr:
            while any([key.startswith(tempStr) for key in keys]):
                tempStr += unsafe[i]
                i+=1

                if tempStr in keys and [key.startswith(tempStr) for key in keys].count(True)==1:
                    idxes.append((i-len(tempStr), i))
                    i-=1
                    break

        i+=1

    for idx in idxes[::-1]:
        key = unsafe[idx[0]:idx[1]]
        target = 'self.varDic["'+key+'"]'
        unsafe = unsafe[:idx[0]] + target + unsafe[idx[1]:]
    return unsafe
