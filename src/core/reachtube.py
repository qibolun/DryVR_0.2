"""
This file contains reach tube class for DryVR
"""

class ReachTube():
    """
    This is class is an object for reach tube
    Ideally it should support to fetch reachtube by mode and variable name
    And it should allow users to plot the reach tube in different ways
    """
    def __init__(self, tube, variables, modes):
        """
            ReachTube class initialization function.

            Args:
            tube (list): raw reach tube (that used to print to file)
            variables (list): list of variables in the reach tube
            modes (list): list of modes in the reach ReachTube
        """
        self.tube = tube
        self.variables = variables
        self.modes = modes

        # Build the raw string representation so user can print it
        
        self.raw = ""
        for line in tube:
            if isinstance(line, str):
                self.raw += line + "\n"
            else:
                self.raw += " ".join(map(str, line))+'\n'

        # Build dictionary object so you can easily pull out part of the list
        self.tubeDic = {}
        for mode in modes:
            self.tubeDic[mode] = {}
            for var in variables+["t"]:
                self.tubeDic[mode][var] = []

        curMode = ""
        for line in tube:
            if isinstance(line, unicode) or isinstance(line, str):
                curMode = line.split('->')[-1].split(',')[0] # Get current mode name
                for var in ['t']+self.variables:
                    self.tubeDic[curMode][var].append(line)
            else:
                for var, val in zip(['t']+self.variables, line):
                    self.tubeDic[curMode][var].append(val)


    def __str__(self):
        """
            print the raw tube
        """
        return self.raw

    def filter(self, mode=None, variable=None, containLabel=True):
        """
            This is a filter function that allows you to select 
            Args:
            mode (str, list): single mode name or list of mode name
            variable (str, list): single variable or list of variables
        """
        if mode == None:
            mode = self.modes
        if variable == None:
            variable = ["t"] + self.variables

        if isinstance(mode, str):
            mode = [mode]
        if isinstance(variable, str):
            variable = [variable]

        res = []
        for m in mode:
            temp = []
            for i in range(len(self.tubeDic[m]["t"])):
                if isinstance(self.tubeDic[m]["t"][i],str):
                    if containLabel:
                        temp.append([self.tubeDic[m]["t"][i]] + variable)
                    continue

                temp.append([self.tubeDic[m][v][i] for v in variable])
            res.append(temp)
        return res


if __name__ == "__main__":
    # Test script 
    f = open("../../output/reachtube.txt").readlines()
    tube = []
    for line in f:
        line = line.strip()
        if ',' in line:
            tube.append(line)
        else:
            tube.append(map(float, line.split()))
    reach = ReachTube(tube, ["Temp"], ["On", "Off"])
    print reach.filter(mode="On")
    # print(reach)


