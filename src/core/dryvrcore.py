"""
This file contains core functions used by DryVR
"""

import random

from collections import defaultdict
from igraph import *
from src.common.constant import *
from src.common.io import writeToFile,readFromFile
from src.common.utils import randomPoint,calcDelta,calcCenterPoint,buildModeStr
from src.discrepancy.Global_Disc import *

def buildGraph(vertex, edge, guards, timeHorizon):
	g = Graph(directed = True)
	g.add_vertices(len(vertex))
	remainTime = [0 for _ in range(len(vertex))]
	g.add_edges(edge)

	# Check the graph is dag
	assert g.is_dag()==True, "Graph is not DAG!"

	g.vs['label'] = vertex
	g.vs['name'] = vertex
	g.vs['remainTime'] = remainTime
	g.es['label'] = guards

	computerOrder = g.topological_sorting(mode=OUT)
	for node in computerOrder:
		if len(g.predecessors(node)) == 0:
			g.vs[node]["remainTime"]  = timeHorizon

	if PLOTGRAPH:
		graph = plot(g, 'output/curGraph.png', margin=40)
		graph.save()

	return g

def simulate(g, initCondition, timeHorizon, guard, simFuc):
	# Taken graph, initial condition, simulate time, guard
	# simFuc is the simulation function
	# which takes label, initial condition and simulation time

	retval = defaultdict(list)
	computerOrder = g.topological_sorting(mode=OUT)
	curVertex = computerOrder[0]
	remainTime = timeHorizon
	curTime = 0

	# Plus 1 becasue we need to consider about time
	dimensions = len(initCondition)+1

	simResult = []
	while remainTime>0:

		if DEBUG:
			print NEWLINE
			print 'Current State', g.vs[curVertex]['label'], remainTime

		if not initCondition:
			# Ideally this should not happen
			break

		curSuccessors = g.successors(curVertex)

		if len(curSuccessors) == 0:
			transiteTime = remainTime
			curGuardStr = None
		else:
			# Randomly pick a path and time to transit
			curSuccessor = random.choice(curSuccessors)
			edgeID = g.get_eid(curVertex,curSuccessor)
			curGuardStr = g.es[edgeID]['label']
			transiteTime = remainTime
		

		curLabel = g.vs[curVertex]['label']
		curSimResult = simFuc(curLabel, initCondition, transiteTime)
		initCondition, trunckedResult = guard.guardSimuTube(
			curSimResult,
			curGuardStr
		)
		# Get real transite time from truncked result
		transiteTime = trunckedResult[-1][0]
		retval[curLabel] += trunckedResult

		for simRow in trunckedResult:
			simRow[0] += curTime
			simResult.append(simRow)

		remainTime -= transiteTime
		curTime += transiteTime
		curVertex = curSuccessor

	writeToFile(simResult, SIMRESULTOUTPUT)
	return retval

def calcReachTube(g, initialSet, timeHorizon, guard, simFuc):
	# Taken graph, initial condition, calculate the reachtube till time
	# simFuc is the simulation function
	# which takes label, initial condition and simulation time
	retval = defaultdict(list)
	numVertex = g.vcount()
	initValues = [[] for _ in range(numVertex)]
	

	computerOrder = g.topological_sorting(mode=OUT)
	vertexOrder = 0
	remainTime = timeHorizon
	breakflag = False
	reachtubeResult = []
	initValues[0].append((initialSet, buildModeStr(g, computerOrder[vertexOrder])))

	while remainTime > 0 and vertexOrder<len(computerOrder):
		curVertex = computerOrder[vertexOrder]
		curSuccessors = g.successors(curVertex)
		curPredecessors = g.predecessors(curVertex)

		if DEBUG:
			print NEWLINE
			print("Current State is the %d th mode with name %s" %(curVertex, g.vs[curVertex]["name"]))

		if not initValues[curVertex]:
			# Ideally this should not happen
			break

		for initialSet, transitionLabel in initValues[curVertex]:
			# Loop through all the initial sets we have for this mode
			# This is because mutiple previous mode can go to current mode
			reachtubeResult.append(transitionLabel)
			curDelta = calcDelta(initialSet[0], initialSet[1])

			if DEBUG:
				print "Initial Condition is", initialSet
				print "Initial Delta is ", curDelta

			curCenter = calcCenterPoint(initialSet[0], initialSet[1])
			curLabel = g.vs[curVertex]['label']

			traces = []
			traces.append(simFuc(curLabel, curCenter, remainTime))
			for _ in range(SIMTRACENUM):
				newInitPoint = randomPoint(initialSet[0], initialSet[1])
				traces.append(simFuc(curLabel, newInitPoint, remainTime))

			k, gamma = Global_Discrepancy(curLabel, curDelta, 0, 2, traces)
			curReachTube = bloatToTube(curLabel, k, gamma, curDelta, traces)

			candidateTube = []
			for curSuccessor in curSuccessors:
				edgeID = g.get_eid(curVertex, curSuccessor)
				curGuardStr = g.es[edgeID]['label']
				nextInit, trunckedResult, transiteTime = guard.guardReachTube(
					curReachTube,
					curGuardStr,
				)
				g.vs[curSuccessor]['remainTime'] = max(
					g.vs[curSuccessor]['remainTime'], 
					g.vs[curVertex]['remainTime']-transiteTime,
				)
				if len(trunckedResult)>len(candidateTube):
					candidateTube = trunckedResult
				nextTransiteLabel = buildModeStr(g, curVertex)+'->'+buildModeStr(g, curSuccessor)
				initValues[curSuccessor].append((nextInit, nextTransiteLabel))
			if not candidateTube:
				candidateTube = curReachTube

			retval[curLabel] += candidateTube
			reachtubeResult += candidateTube
			vertexOrder += 1
			if vertexOrder < len(computerOrder):
				remainTime = g.vs[computerOrder[vertexOrder]]['remainTime']
	return retval, reachtubeResult
