"""
This file contains a single function that verifies model
"""

from src.common.constant import *
from src.common.io import parseInputFile
from src.common.utils import importSimFunction, randomPoint
from src.core.dryvrcore import *
from src.core.guard import Guard
from src.core.initialset import InitialSet
from src.core.uniformchecker import UniformChecker

def verify(inputFile):
	params = parseInputFile(inputFile)
	graph = buildGraph(
		params.vertex,
		params.edge,
		params.guards,
		params.timeHorizon,
	)
	simFunction = importSimFunction(params.path)
	checker = UniformChecker(params.unsafeSet, params.variables)
	guard = Guard(params.variables)

	# Step 1) Simulation Test 
	# Random generate points, then simulate and check the result
	for _ in range(SIMUTESTNUM):
		randInit = randomPoint(params.initialSet[0], params.initialSet[1])

		if DEBUG:
			print 'Random checking round ', _, 'at point ', randInit

		simResult = simulate(
			graph,
			randInit,
			params.timeHorizon,
			guard,
			simFunction,
		)
		for mode in simResult:
			safety = checker.checkSimuTube(simResult[mode], mode)
			if safety == -1:
				print 'Current simulation is not safe. Program halt'
				exit()

	# # # Step 2) Check Reach Tube
	# # # Calculate the over approximation of the reach tube and check the result