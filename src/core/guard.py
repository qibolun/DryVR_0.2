"""
This file contains guard class for DryVR
"""

import random
import sympy

from src.common.utils import handleReplace
from z3 import *

class Guard():
    """
    This is class to calculate the set in the 
    reach tube that intersect with the guard
    """
    def __init__(self, variables):
        """
        Guard checker class initialization function.

        Args:
            variables (list): list of varibale name
        """
        self.varDic = {'t':Real('t')}
        self.variables = variables
        for var in variables:
            self.varDic[var] = Real(var)

    def _buildGuard(self, guardStr):
        """
        Build solver for current guard based on guard string

        Args:
            guardStr (str): the guard string.
            For example:"And(v>=40-0.1*u, v-40+0.1*u<=0)"

        Returns:
            A Z3 Solver obj that check for guard.
            A symbol index dic obj that indicates the index
            of variables that involved in the guard.
        """
        curSolver = Solver()
        # This magic line here is because sympy will evaluate == to be False
        # Therefore we are not be able to get free symbols from it
        # Thus we need to replace "==" to something else
        sympyGuardStr = guardStr.replace("==",">=")

        symbols = list(sympy.sympify(sympyGuardStr, evaluate=False).free_symbols)
        symbols = [str(s) for s in symbols]
        symbolsIdx = {s:self.variables.index(s)+1 for s in symbols if s in self.variables}
        if 't' in symbols:
            symbolsIdx['t'] = 0


        guardStr = handleReplace(guardStr,self.varDic.keys())
        curSolver.add(eval(guardStr))
        return curSolver, symbolsIdx

    def guardSimuTrace(self, trace, guardStr):
        """
        Check the guard for simulation trace.
        Note we treat the simulation trace as the set as well.
        Consider we have a simulation trace as following
        [0.0, 1.0, 1.1]
        [0.1, 1.02, 1.13]
        [0.2, 1.05, 1.14]
        ...
        We can build set like
        lowerbound: [0.0, 1.0, 1.1]
        upperbound: [0.1, 1.02, 1.13]

        lowerbound: [0.1, 1.02, 1.13]
        upperbound: [0.2, 1.05, 1.14]
        And check guard for these set. This is because if the guard
        is too small, it is likely for simulation point ignored the guard.
        For example:
            .     .     .     . |guard| .    .   .
            In this case, the guard gets ignored

        Args:
            trace (list): the simulation trace
            guardStr (str): the guard string.
            For example:"And(v>=40-0.1*u, v-40+0.1*u<=0)"

        Returns:
            A initial point for next mode,
            The truncated simulation trace
        """
        if not guardStr:
            return None, trace
        curSolver, symbols = self._buildGuard(guardStr)
        guardSet = {}

        for idx in range(len(trace)-1):
            lower = trace[idx]
            upper = trace[idx+1]
            curSolver.push()
            for symbol in symbols:
                curSolver.add(self.varDic[symbol] >= min(lower[symbols[symbol]], upper[symbols[symbol]]))
                curSolver.add(self.varDic[symbol] <= max(lower[symbols[symbol]], upper[symbols[symbol]]))
            if curSolver.check() == sat:
                curSolver.pop()
                guardSet[idx] = upper
            else:
                curSolver.pop()
                if guardSet:
                    # Guard set is not empty, randomly pick one and return
                    idx, point = random.choice(list(guardSet.items()))
                    # Return the initial point for next mode, and truncked trace
                    return point[1:], trace[:idx+1]

        # No guard hits for current tube
        return None, trace

    def guardSimuTraceTime(self, trace, guardStr):
        """
        Return the length of the truncated traces

        Args:
            trace (list): the simulation trace
            guardStr (str): the guard string.
            For example:"And(v>=40-0.1*u, v-40+0.1*u<=0)"

        Returns:
            the length of the truncated traces.
        """
        nextInit, trace = self.guardSimuTrace(trace, guardStr)
        return len(trace)



    def guardReachTube(self, tube, guardStr):
        """
        Check the guard intersection of the reach tube


        Args:
            tube (list): the reach tube
            guardStr (str): the guard string.
            For example:"And(v>=40-0.1*u, v-40+0.1*u<=0)"

        Returns:
            Next mode initial set represent as [upperbound, lowerbound],
            Truncated tube before the guard,
            The time when elapsed in current mode.

        """
        if not guardStr:
            return None, tube

        curSolver, symbols = self._buildGuard(guardStr)
        guardSetLower = []
        guardSetUpper = []
        for i in range(0,len(tube),2):
            curSolver.push()
            lowerBound = tube[i]
            upperBound = tube[i+1]
            for symbol in symbols:
                curSolver.add(self.varDic[symbol] >= lowerBound[symbols[symbol]])
                curSolver.add(self.varDic[symbol] <= upperBound[symbols[symbol]])

            if curSolver.check() == sat:
                # The reachtube hits the guard
                curSolver.pop()
                guardSetLower.append(lowerBound)
                guardSetUpper.append(upperBound)
            else:
                curSolver.pop()
                if guardSetLower:
                    # Guard set is not empty, build the next initial set and return
                    # At some point we might futher reduce the initial set for next mode
                    initLower = guardSetLower[0][1:]
                    initUpper = guardSetUpper[0][1:]
                    for j in range(1,len(guardSetLower)):
                        for k in range(1,len(guardSetLower[0])):
                            initLower[k-1] = min(initLower[k-1], guardSetLower[j][k])
                            initUpper[k-1] = max(initUpper[k-1], guardSetUpper[j][k])
                    # Return next initial Set, the result tube, and the true transit time
                    return [initLower,initUpper], tube[:i], guardSetLower[0][0]

        # Construct the guard if all later trace sat the guard condition
        if guardSetLower:
            # Guard set is not empty, build the next initial set and return
            # At some point we might futher reduce the initial set for next mode
            initLower = guardSetLower[0][1:]
            initUpper = guardSetUpper[0][1:]
            for j in range(1,len(guardSetLower)):
                for k in range(1,len(guardSetLower[0])):
                    initLower[k-1] = min(initLower[k-1], guardSetLower[j][k])
                    initUpper[k-1] = max(initUpper[k-1], guardSetUpper[j][k])
            # Return next initial Set, the result tube, and the true transit time
            return [initLower,initUpper], tube[:i], guardSetLower[0][0]

        return None, tube, tube[-1][0]
