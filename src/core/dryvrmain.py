"""
This file contains a single function that verifies model
"""

from src.common.constant import *
from src.common.io import parseInputFile,writeReachTubeFile
from src.common.utils import importSimFunction, randomPoint, buildModeStr
from src.core.dryvrcore import *
from src.core.guard import Guard
from src.core.initialset import InitialSet
from src.core.initialsetstack import InitialSetStack
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

	# Step 2) Check Reach Tube
	# Calculate the over approximation of the reach tube and check the result
	print "Verification Begin"
	computeOrder =  graph.topological_sorting(mode=OUT)
	initialMode = computeOrder[0]
	curModeStack = InitialSetStack(initialMode, REFINETHRES, params.timeHorizon)
	curModeStack.stack.append(InitialSet(params.initialSet[0], params.initialSet[1]))
	curModeStack.bloatedTube.append(buildModeStr(graph, initialMode))
	while True:
		backwardFlag = SAFE
		while curModeStack.stack:
			print "Mode", curModeStack.mode, "has stack size", len(curModeStack.stack)
			if not curModeStack.isValid():
				print curModeStack.mode, "is not valid anymore"
				backwardFlag = UNKNOWN
				break

			curStack = curModeStack.stack
			curVertex = curModeStack.mode
			curRemainTime = curModeStack.remainTime
			curLabel = graph.vs[curVertex]['label']
			curSuccessors = graph.successors(curVertex)
			curInitial = [curStack[-1].lowerBound, curStack[-1].upperBound]
			curBloatedTube = clacBloatedTube(curLabel, curInitial, curRemainTime, simFunction)

			candidateTube = []

			for curSuccessor in curSuccessors:
				edgeID = graph.get_eid(curVertex, curSuccessor)
				curGuardStr = graph.es[edgeID]['label']
				nextInit, trunckedResult, transiteTime = guard.guardReachTube(
					curBloatedTube,
					curGuardStr,
				)
				nextModeStack = InitialSetStack(
					curSuccessor,
					CHILDREFINETHRES,
					curRemainTime-transiteTime,
				)
				nextModeStack.parent = curModeStack
				nextModeStack.stack.append(InitialSet(nextInit[0], nextInit[1]))
				nextModeStack.bloatedTube.append(curModeStack.bloatedTube[0]+'->'+buildModeStr(graph, curSuccessor))
				curStack[-1].child[curSuccessor] = nextModeStack
				if len(trunckedResult)>len(candidateTube):
					candidateTube = trunckedResult

			if not candidateTube:
				candidateTube = curBloatedTube

			# Check the safety for current bloated tube
			safety = checker.checkReachTube(candidateTube, curLabel)
			if safety == UNSAFE:
				print "System is not safe in Mode ", curLabel
				exit()

			elif safety == UNKNOWN:
				print curModeStack.mode, "check bloated tube unknown"
				discardInitial = curModeStack.stack.pop()
				initOne, initTwo = discardInitial.refine()
				curModeStack.stack.append(initOne)
				curModeStack.stack.append(initTwo)

			elif safety == SAFE:
				print "Mode", curModeStack.mode, "check bloated tube safe"
				if curModeStack.stack[-1].child:
					curModeStack.stack[-1].bloatedTube += candidateTube
					nextMode, nextModeStack = curModeStack.stack[-1].child.popitem()
					curModeStack = nextModeStack
					print "Child exist in cur mode inital", curModeStack.mode, "is curModeStack Now"
				else:
					curModeStack.bloatedTube += candidateTube
					curModeStack.stack.pop()
					print "No child in mode initial, pop"
			else:
				print "Some thing bad happen in Mode ", curLabel
				exit()

		if curModeStack.parent is None:
			if backwardFlag == SAFE:
				print "System is Safe!"
				writeReachTubeFile(curModeStack.bloatedTube, REACHTUBEOUTPUT)
				return
			elif backwardFlag == UNKNOWN:
				print "Hit refine threshold, system halt, result unknown"
				exit()
		else:
			if backwardFlag == SAFE:
				prevModeStack = curModeStack.parent
				prevModeStack.stack[-1].bloatedTube += curModeStack.bloatedTube
				print 'back flag safe from',curModeStack.mode,'to',prevModeStack.mode
				if len(prevModeStack.stack[-1].child) == 0:
					# There is no next mode from this initial set
					prevModeStack.bloatedTube += prevModeStack.stack[-1].bloatedTube
					prevModeStack.stack.pop()
					curModeStack = prevModeStack
					print "No child in prev mode initial, pop,", prevModeStack.mode, "is curModeStack Now"
				else:
					# There is another mode transition from this initial set
					nextMode, nextModeStack = prevModeStack.stack[-1].child.popitem()
					curModeStack = nextModeStack
					print "Child exist in prev mode inital", nextModeStack.mode, "is curModeStack Now"
			elif backwardFlag == UNKNOWN:
				prevModeStack = curModeStack.parent
				print 'back flag unknown from',curModeStack.mode,'to',prevModeStack.mode
				discardInitial = prevModeStack.stack.pop()
				initOne, initTwo = discardInitial.refine()
				prevModeStack.stack.append(initOne)
				prevModeStack.stack.append(initTwo)
				curModeStack = prevModeStack


	# initialStack = [
	# 	InitialSet(
	# 		params.initialSet[0],
	# 		params.initialSet[1],
	# 		0,
	# 	)
	# ]
	# reachTubeResult = []

	# while initialStack:
	# 	curInitial = initialStack.pop()
	# 	if curInitial.refineTime >= REFINETHRES:
	# 		print "Maximum refine time hits, verification halt. Result unknown"
	# 		exit()

	# 	if DEBUG:
	# 		print NEWLINE
	# 		print str(curInitial)

	# 	tubeDic, curReachTubeResult = calcReachTube(
	# 		graph,
	# 		[curInitial.lowerBound, curInitial.upperBound],
	# 		params.timeHorizon,
	# 		guard,
	# 		simFunction,
	# 	)

	# 	safe = 1
	# 	for key in tubeDic:
	# 		curTube = tubeDic[key]
	# 		safety = checker.checkReachTube(curTube, key)
	# 		if safety == -1:
	# 			print "System is not safe from reach tube computation, halt"
	# 			exit()

	# 		elif safety == 0:
	# 			print "System is unknown at ", key
	# 			safe = 0

	# 	if safe == 0:
	# 		print "System is unknown. Refine the initial set"
	# 		initOne, initTwo = curInitial.refine()
	# 		initialStack.append(initOne)
	# 		initialStack.append(initTwo)
	# 	else:
	# 		reachTubeResult += curReachTubeResult

	# print "System is Safe!"
	# writeReachTubeFile(reachTubeResult, REACHTUBEOUTPUT)
