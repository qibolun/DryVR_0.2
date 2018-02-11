"""
This file contains IO functions for DryVR
"""

import json

from utils import DryVRInput, RrtInput

def writeReachTubeFile(result, path):
    """
    Write reach tube to a file 
    
    reach tube example:
        mode1
        [0.0, 1, 2]
        [0.1, 2, 3]
        [0.1, 2, 3]
        ....
        mode1->mode2
        [1.0, 3, 4]
        ....
        
    Args:
        result (list): list of reachable state.
        path (str): file name.

    Returns:
        None

    """
    with open(path, 'w') as f:
        for line in result:
            if isinstance(line, unicode):
                f.write(line+'\n')
            elif isinstance(line, list):
                f.write(' '.join(map(str,line))+'\n')

def writeRrtResultFile(modes, traces, path):
    """
    Write control synthesis result to a file 
    
    Args:
        modes (list): list of mode.
        traces (list): list of traces corresponding to modes
        path (str): file name.

    Returns:
        None

    """
    with open(path, 'w') as f:
        for mode, trace in zip(modes, traces):
            f.write(mode + '\n')
            for line in trace:
                f.write(" ".join(map(str, line))+'\n')

def parseVerificationInputFile(path):
    """
    Parse the json input for DryVR verification
    
    Args:
        path (str): input file name (Must be json format).

    Returns:
        DryVR verification input object

    """
    with open(path, 'r') as f:
        data = json.load(f)

        # If resets is missing, fill with empty resets
        if not 'resets' in data:
            data['resets'] = ["" for _ in range(len(data["edge"]))]

        # If initialMode is missing, fill with empty initial mode
        if not 'initialMode' in data:
            data['initialMode'] = ""

        # If deterministic is missing, default to non-deterministic
        if not 'deterministic' in data:
            data['deterministic'] = False

        # If bloating method is missing, default global descrepancy
        if not 'bloatingMethod' in data:
            data['bloatingMethod'] = 'GLOBAL'

        # if kvalue is missing, default to 1.0
        if not 'kvalue' in data:
            data['kvalue'] = [1.0 for i in range(len(data['variables']))]
            if data['bloatingMethod'] == "PW":
                print "Warning: No kvalue provided when using PW descrepancy, default kvalue 1.0 for all variable."
                raw_input("Press Enter to continue...")


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
            bloatingMethod=data['bloatingMethod'],
            kvalue=data['kvalue'],
        )

def parseRrtInputFile(path):
    """
    Parse the json input for DryVR controller synthesis
    
    Args:
        path (str): input file name (Must be json format).

    Returns:
        DryVR controller synthesis input object

    """
    with open(path, 'r') as f:
        data = json.load(f)

        # If bloating method is missing, default global descrepancy
        if not 'bloatingMethod' in data:
            data['bloatingMethod'] = 'GLOBAL'

        # if kvalue is missing, default to 1.0
        if not 'kvalue' in data:
            data['kvalue'] = [1.0 for i in range(len(data['variables']))]
            if data['bloatingMethod'] == "PW":
                print "Warning: No kvalue provided when using PW descrepancy, default kvalue 1.0 for all variable."
                raw_input("Press Enter to continue...")

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
            bloatingMethod=data['bloatingMethod'],
            kvalue=data['kvalue'],
        )
