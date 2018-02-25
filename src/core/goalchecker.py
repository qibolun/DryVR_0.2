"""
This file contains uniform checker class for DryVR
"""


from src.common.utils import handleReplace, neg
from z3 import *

class GoalChecker():
	"""
	This is class to check if the goal set is reached
	by reach tube
    """
	def __init__(self, goal, variables):
		"""
		Goal checker class initialization function.

        Args:
            goal (str): a str describle the goal set.
            For example: "And(x_1>=19.5, x_1<=20.5, x_2>=-1.0, x_2<=1.0)"
            variables (list): list of varibale name
        """
		self.varDic = {'t':Real('t')}
		self.variables = variables
		for var in variables:
			self.varDic[var] = Real(var)

		goal = handleReplace(goal, self.varDic.keys())

		self.intersectChecker = Solver()
		self.containChecker = Solver()

		self.intersectChecker.add(eval(goal))
		self.containChecker.add(eval(neg(goal)))

	def goalReachTube(self, tube):
		"""
		Check if the reach tube satisified the goal

        Args:
            tube (list): the reach tube.

        Returns:
            A bool indicates if the goal is reached
            The truncated tube if the goal is reached, otherwise the whole tube
        """
		for i in range(0, len(tube), 2):
			lower = tube[i]
			upper = tube[i+1]
			if self._checkIntersection(lower, upper):
				if self._checkContainment(lower, upper):
					return True, tube[:i+2]
		return False, tube

	def _checkIntersection(self, lower, upper):
		"""
		Check if the goal set intersect with the current set
		#FIXME Maybe this is not neccessary since we only want to check
		the fully contained case
		Bolun 02/13/2018 

        Args:
            lower (list): the list represent the set's lowerbound.
            upper (list): the list represent the set's upperbound.

        Returns:
            A bool indicates if the set intersect with the goal set
        """
		curSolver = self.intersectChecker
		curSolver.push()
		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])
		for i in range(1, len(lower)):
			curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
			curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])
		if curSolver.check() == sat:
			curSolver.pop()
			return True
		else:
			curSolver.pop()
			return False

	def _checkContainment(self, lower, upper):
		"""
		Check if the current set contained in goal set.

        Args:
            lower (list): the list represent the set's lowerbound.
            upper (list): the list represent the set's upperbound.

        Returns:
            A bool indicates if the set if contained in the goal set
        """
		curSolver = self.containChecker
		curSolver.push()
		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])
		for i in range(1, len(lower)):
			curSolver.add(self.varDic[self.variables[i-1]]>=lower[i])
			curSolver.add(self.varDic[self.variables[i-1]]<=upper[i])
		if curSolver.check() == sat:
			curSolver.pop()
			return False
		else:
			curSolver.pop()
			return True

