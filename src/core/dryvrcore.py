"""
This file contains core functions used by DryVR
"""

import numpy
import random

from collections import defaultdict
from igraph import *
from src.common.constant import *
from src.common.io import writeReachTubeFile
from src.common.utils import randomPoint,calcDelta,calcCenterPoint,buildModeStr
from src.discrepancy.Global_Disc import *
from src.discrepancy.PW_Discrepancy import PW_Bloat_to_tube

def buildGraph(vertex, edge, guards, timeHorizon, resets):
	g = Graph(directed = True)
	g.add_vertices(len(vertex))
	g.add_edges(edge)

	g.vs['label'] = vertex
	g.vs['name'] = vertex
	labels = []
	for i in range(len(guards)):
		curGuard = guards[i]
		curReset = resets[i]
		if not curReset:
			labels.append(curGuard)
		else:
			labels.append(curGuard+'|'+curReset)

	g.es['label'] = labels
	g.es['guards'] = guards
	g.es['resets'] = resets

	if PLOTGRAPH:
		graph = plot(g, GRAPHOUTPUT, margin=40)
		graph.save()
	return g

def buildRrtGraph(modes, traces):
	# Build Rrt Graph based on modes and traces
	g = Graph(directed = True)
	g.add_vertices(len(modes))
	edges = []
	for i in range(1, len(modes)):
		edges.append([i-1, i])
	g.add_edges(edges)

	g.vs['label'] = modes
	g.vs['name'] = modes

	# Build guard
	guard = []
	for i in range(len(traces)-1):
		lower = traces[i][-2][0]
		upper = traces[i][-1][0]
		guard.append("And(t>" + str(lower) +", t<=" + str(upper) + ")")
	g.es['label'] = guard
	graph = plot(g, RRTGRAPHPOUTPUT, margin=40)
	graph.save()


def simulate(g, initCondition, timeHorizon, guard, simFuc, reseter, initialMode, deterministic):
	# Taken graph, initial condition, simulate time, guard
	# simFuc is the simulation function
	# which takes label, initial condition and simulation time

	retval = defaultdict(list)

	# If you do not delcare initialMode, then we will just use topological sort to find starting point
	if not initialMode:
		computerOrder = g.topological_sorting(mode=OUT)
		curVertex = computerOrder[0]
	else:
		curVertex = g.vs.find(label=initialMode).index

	remainTime = timeHorizon
	curTime = 0

	# Plus 1 becasue we need to consider about time
	dimensions = len(initCondition)+1

	simResult = []
	# Avoid numeric error
	while remainTime>0.01:

		if DEBUG:
			print NEWLINE
			print curVertex, remainTime
			print 'Current State', g.vs[curVertex]['label'], remainTime

		if initCondition is None:
			# Ideally this should not happen
			break

		curSuccessors = g.successors(curVertex)
		transiteTime = remainTime
		curLabel = g.vs[curVertex]['label']

		curSimResult = simFuc(curLabel, initCondition, transiteTime)
		if isinstance(curSimResult,numpy.ndarray):
			curSimResult = curSimResult.tolist()

		if len(curSuccessors) == 0:
			# Some model return numpy array, convert to list
			initCondition, trunckedResult = guard.guardSimuTube(
				curSimResult,
				None
			)
			curSuccessor = None

		else:
			# First find all possible transition
			# Second randomly pick a path and time to transit
			nextModes = []
			for curSuccessor in curSuccessors:
				edgeID = g.get_eid(curVertex,curSuccessor)
				curGuardStr = g.es[edgeID]['guards']
				curResetStr = g.es[edgeID]['resets']

				nextInit, trunckedResult = guard.guardSimuTube(
					curSimResult,
					curGuardStr
				)

				# for line in trunckedResult:
				# 	print line 
				nextInit = reseter.resetSimTrace(curResetStr, nextInit)
				# If there is a transition
				if nextInit:
					nextModes.append((curSuccessor, nextInit, trunckedResult))
			if nextModes:
				# It is a non-deterministic system, randomly choose next state to transit
				if deterministic == False:
					curSuccessor, initCondition, trunckedResult = random.choice(nextModes)
				# This is deterministic system, choose earliest transition
				else:
					shortestTime = float('inf')
					for s, i, t in nextModes:
						curTubeTime = t[-1][0]
						if curTubeTime<shortestTime:
							curSuccessor = s
							initCondition = i
							trunckedResult = t
							shortestTime = curTubeTime
			else:
				curSuccessor = None
				initCondition = None

		# Get real transite time from truncked result
		transiteTime = trunckedResult[-1][0]
		retval[curLabel] += trunckedResult
		simResult.append(curLabel)
		for simRow in trunckedResult:
			simRow[0] += curTime
			simResult.append(simRow)

		remainTime -= transiteTime
		print "transit time", transiteTime, "remain time", remainTime
		curTime += transiteTime
		curVertex = curSuccessor

	writeReachTubeFile(simResult, SIMRESULTOUTPUT)
	return retval

def clacBloatedTube(modeLabel, initialSet, timeHorizon, simFuc, bloatingMethod, kvalue, guardChecker=None, guardStr=None):
	# Taking modeLabel, initial set, time horizon information
	# Calculate the bloated tube
	curCenter = calcCenterPoint(initialSet[0], initialSet[1])
	curDelta = calcDelta(initialSet[0], initialSet[1])
	traces = []
	traces.append(simFuc(modeLabel, curCenter, timeHorizon))
	for _ in range(SIMTRACENUM):
		newInitPoint = randomPoint(initialSet[0], initialSet[1])
		# print "========new rad point=========="
		# print newInitPoint
		#print newInitPoint
		traces.append(simFuc(modeLabel, newInitPoint, timeHorizon))

	if guardChecker is not None:
		# pre truncked traces to get better bloat result
		# print guardStr, "trace check"
		maxIdx = -1
		for trace in traces:
			# print "simulation trace"
			# for t in trace:
			# 	print t
			retIdx = guardChecker.guardSimuTraceTime(trace, guardStr)
			maxIdx = max(maxIdx, retIdx+1)
		# print "max Idx is ", maxIdx
		for i in range(len(traces)):
			traces[i] = traces[i][:maxIdx]
		#print traces

	if bloatingMethod == GLOBAL:
		if BLOATDEBUG:
			k, gamma = Global_Discrepancy(modeLabel, curDelta, 1, PLOTDIM, traces)
		else:
			k, gamma = Global_Discrepancy(modeLabel, curDelta, 0, PLOTDIM, traces)
		# print curDelta
		curReachTube = bloatToTube(modeLabel, k, gamma, curDelta, traces)
	elif bloatingMethod == PW:
		if BLOATDEBUG:
			curReachTube = PW_Bloat_to_tube(curDelta, 1, PLOTDIM, traces, kvalue)
		else:
			curReachTube = PW_Bloat_to_tube(curDelta, 0, PLOTDIM, traces, kvalue)
	return curReachTube
