"""
This file contains a single function that verifies model
"""
import random

from src.common.constant import *
from src.common.io import parseInputFile, writeReachTubeFile, parseRrtInputFile, writeRrtResultFile
from src.common.utils import importSimFunction, randomPoint, buildModeStr
from src.core.distance import DistChecker
from src.core.dryvrcore import *
from src.core.goalchecker import GoalChecker
from src.core.guard import Guard
from src.core.initialset import InitialSet
from src.core.initialsetstack import InitialSetStack, RrtSetStack
from src.core.reset import Reset
from src.core.uniformchecker import UniformChecker

def verify(inputFile):
	params = parseInputFile(inputFile)
	graph = buildGraph(
		params.vertex,
		params.edge,
		params.guards,
		params.timeHorizon,
		params.resets
	)

	assert graph.is_dag()==True or params.initialMode!="", "Graph is not DAG and you do not have initial mode!"

	simFunction = importSimFunction(params.path)
	checker = UniformChecker(params.unsafeSet, params.variables)
	guard = Guard(params.variables)
	reseter = Reset(params.variables)

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
			reseter,
			params.initialMode,
			params.deterministic
		)
		for mode in simResult:
			safety = checker.checkSimuTube(simResult[mode], mode)
			if safety == -1:
				print 'Current simulation is not safe. Program halt'
				exit()
	# Step 2) Check Reach Tube
	# Calculate the over approximation of the reach tube and check the result
	print "Verification Begin"
	if not params.initialMode:
		computeOrder =  graph.topological_sorting(mode=OUT)
		initialMode = computeOrder[0]
	else:
		initialMode = graph.vs.find(label=params.initialMode).index

	curModeStack = InitialSetStack(initialMode, REFINETHRES, params.timeHorizon)
	curModeStack.stack.append(InitialSet(params.initialSet[0], params.initialSet[1]))
	curModeStack.bloatedTube.append(buildModeStr(graph, initialMode))
	while True:
		backwardFlag = SAFE
		while curModeStack.stack:
			print str(curModeStack)
			if not curModeStack.isValid():
				print curModeStack.mode, "is not valid anymore"
				backwardFlag = UNKNOWN
				break

			if isinstance(curModeStack.bloatedTube[-1], list):
				curModeStack.bloatedTube.append(curModeStack.bloatedTube[0])

			curStack = curModeStack.stack
			curVertex = curModeStack.mode
			curRemainTime = curModeStack.remainTime
			curLabel = graph.vs[curVertex]['label']
			curSuccessors = graph.successors(curVertex)
			curInitial = [curStack[-1].lowerBound, curStack[-1].upperBound]
			curBloatedTube = clacBloatedTube(curLabel, curInitial, curRemainTime, simFunction)

			candidateTube = []
			shortestTime = float("inf")
			shortestTube = None

			for curSuccessor in curSuccessors:
				edgeID = graph.get_eid(curVertex, curSuccessor)
				curGuardStr = graph.es[edgeID]['guards']
				curResetStr = graph.es[edgeID]['resets']
				nextInit, trunckedResult, transiteTime = guard.guardReachTube(
					curBloatedTube,
					curGuardStr,
				)
				if nextInit == None:
					continue

				nextInit = reseter.resetReachTube(curResetStr, nextInit[0], nextInit[1])

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

				if trunckedResult[-1][0] < shortestTime:
					shortestTime = trunckedResult[-1][0]
					shortestTube = trunckedResult

			# Handle deterministic system
			if params.deterministic and len(curStack[-1].child)>0:
				nextModesInfo = []
				for nextMode in curStack[-1].child:
					nextModesInfo.append((curStack[-1].child[nextMode].remainTime, nextMode))
				# This mode gets transit first, only keep this mode
				maxRemainTime, maxTimeMode = max(nextModesInfo)
				# Pop other modes becuase of deterministic system
				for time, nextMode in nextModesInfo:
					if nextMode == maxTimeMode:
						continue
					curStack[-1].child.pop(nextMode)
				candidateTube = shortestTube
				print "Handle deterministic system, next mode", curStack[-1].child.keys()

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
				print "Something bad happen in Mode ", curLabel
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


def rrtSimulation(inputFile):
	params = parseRrtInputFile(inputFile)
	simFunction = importSimFunction(params.path)
	checker = UniformChecker(params.unsafeSet, params.variables)
	goalSetChecker = GoalChecker(params.goalSet, params.variables)
	distanceChecker = DistChecker(params.goal, params.variables)
	simFunction = importSimFunction(params.path)
	availableModes = params.modes
	initialMode = params.initialMode
	remainTime = params.timeHorizon
	minTimeThres = params.minTimeThres

 	goalReached = False
 	curModeStack = RrtSetStack(initialMode, remainTime, minTimeThres, 0)
 	curModeStack.initial = (params.initialSet[0], params.initialSet[1])

 	while True:
 		print str(curModeStack)
		if not curModeStack:
			break

 		if curModeStack.remainTime < minTimeThres:
 			print "Back to previous mode because we cannot stay longer than the min time thres"
 			curModeStack = curModeStack.parent
 			continue

 		if len(curModeStack.visited) == len(availableModes):
 			if len(curModeStack.candidates)<2:
 				print "Back to previous mode because we do not have any other modes to pick"
	 			curModeStack = curModeStack.parent
	 			# If the tried all possible case with no luck to find path
	 			if not curModeStack:
	 				break
	 			continue
	 		else:
	 			print "Pick a new point from candidates"
	 			curModeStack.candidates.pop(0)
	 			curModeStack.visited = set()
	 			curModeStack.children = {}
	 			continue


 		# Generate bloated tube if we have not done so
 		if not curModeStack.bloatedTube:
 			print "no bloated tube find in this mode, generate one"
 			curBloatedTube = clacBloatedTube(
 				curModeStack.mode,
 				curModeStack.initial,
 				curModeStack.remainTime,
 				simFunction
 			)
 			curBloatedTube = checker.cutTubeTillUnsafe(curBloatedTube)
 			# we cannot stay in this mode for min thres time, back to the previous mode
 			if not curBloatedTube or curBloatedTube[-1][0] < minTimeThres:
 				print "bloated tube is not long enough, discard the mode"
 				curModeStack = curModeStack.parent
 				continue
 			curModeStack.bloatedTube = curBloatedTube

 			# Generate candidates point for next mode
 			randomSections = curModeStack.randomPicker(RANDSECTIONNUM)

 			if not randomSections:
 				print "bloated tube is not long enough, discard the mode"
 				curModeStack = curModeStack.parent
 				continue

 			randomSections.sort(key=lambda x: distanceChecker.calcDistance(x[0], x[1]))
 			curModeStack.candidates = randomSections
 			print "Generate new bloated tube and candidate, with candidates length", len(curModeStack.candidates)


 			# Check if the current tube reaches goal
 			result, tube = goalSetChecker.goalReachTube(curBloatedTube)
 			if result:
 				curModeStack.bloatedTube = tube
 				goalReached = True
 				break

 		# We have visited all next mode we have, generate some thing new
 		if len(curModeStack.visited) == len(curModeStack.children):
 			leftMode = set(availableModes) - set(curModeStack.children.keys())
 			randomModes = random.sample(leftMode, min(len(leftMode), RANDMODENUM))
 			random.shuffle(randomModes)

 			randomSections = curModeStack.randomPicker(RANDSECTIONNUM)
 			for mode in randomModes:
 				candidate = curModeStack.candidates[0]
 				curModeStack.children[mode] = RrtSetStack(mode, curModeStack.remainTime-candidate[1][0], minTimeThres, curModeStack.level+1)
 				curModeStack.children[mode].initial = (candidate[0][1:], candidate[1][1:])
 				curModeStack.children[mode].parent = curModeStack

 		# Random visit a candidate that is not visited before
 		for key in curModeStack.children:
 			if not key in curModeStack.visited:
 				break

 		print "transit point is", curModeStack.candidates[0]
 		curModeStack.visited.add(key)
 		curModeStack = curModeStack.children[key]

 	# Back track to print out trace
 	if goalReached:
 		print("goal reached")
 		traces = []
 		modes = []
 		while curModeStack:
 			modes.append(curModeStack.mode)
 			if not curModeStack.candidates:
 				traces.append([t for t in curModeStack.bloatedTube])
 			else:
 				# Cut the trace till candidate
 				temp = []
 				for t in curModeStack.bloatedTube:
 					if t == curModeStack.candidates[0][0]:
 						temp.append(curModeStack.candidates[0][0])
 						temp.append(curModeStack.candidates[0][1])
 						break
 					else:
 						temp.append(t)
 				traces.append(temp)
 			curModeStack = curModeStack.parent
 		# Reorganize the content in modes list for plotter use
 		modes = modes[::-1]
 		traces = traces[::-1]
 		buildRrtGraph(modes, traces)
 		for i in range(1, len(modes)):
 			modes[i] = modes[i-1]+'->'+modes[i]

 		writeRrtResultFile(modes, traces, RRTOUTPUT)
 	else:
 		print("could not find trace")
