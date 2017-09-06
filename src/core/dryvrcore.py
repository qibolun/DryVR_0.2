"""
This file contains core functions used by DryVR
"""

import random

from collections import defaultdict
from igraph import *
from src.common.constant import *
from src.common.io import writeToFile,readFromFile
from src.common.utils import randomPoint,calcDelta,centerPoint

def buildGraph(vertex, edge, transTime, timeHorizon):
	g = Graph(directed = True)
	g.add_vertices(len(vertex))
	divideIntervals = [1 for _ in range(len(edge))]
	remainTime = [0 for _ in range(len(vertex))]
	g.add_edges(edge)

	# Check the graph is dag
	assert g.is_dag()==True, "Graph is not DAG!"

	g.vs['label'] = vertex
	g.vs['name'] = vertex
	g.vs['remainTime'] = remainTime
	g.es['label'] = transTime
	g.es['trans_time'] = transTime
	g.es['divide'] = divideIntervals

	computerOrder = g.topological_sorting(mode=OUT)
	for node in computerOrder:
		if len(g.predecessors(node)) == 0:
			g.vs[node]["remainTime"]  = timeHorizon

	if PLOTGRAPH:
		graph = plot(g, 'output/curGraph.png', margin=40)
		graph.save()

	return g

def refineGraph(g):
	label = g.es['label']
	divide = g.es['divide']

	maxIdx = [(label[i][1]-label[i][0])/float(divide[i]) for i in range(len(label))]
	idx = maxidx.index(max(maxIdx))
	divide[idx] += 1
	g.es["divide"] = divide

def simulate(g, initCondition, timeHorizon, simFuc):
	# Taken graph, initial condition, simulate time
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
			print 'Current State', g.vs[curVertex]['label']

		curSuccessors = g.successors(curVertex)

		if len(curSuccessors) == 0:
			transiteTime = remainTime
		else:
			# Randomly pick a path and time to transit
			curSuccessor = random.choice(curSuccessors)
			edgeID = g.get_eid(curVertex,curSuccessor)
			curTransitTime = g.es[edgeID]['label']
			transiteTime = randomPoint(curTransitTime[0], curTransitTime[1])

		curLabel = g.vs[curVertex]['label']
		curSimResult = simFuc(curLabel, initCondition, transiteTime)
		retval[curLabel] += curSimResult
		for simRow in curSimResult:
			simRow[0] += curTime
			simResult.append(simRow)

		remainTime -= transiteTime
		initCondition = curSimResult[-1][1:]
		curTime += transiteTime
		curVertex = curSuccessor

	writeToFile(simResult, SIMRESULTOUTPUT)
	return retval


# def calcReachTube(g, initialSet, timeHorizon, simFuc):
# 	# Taken graph, initial condition, calculate the reachtube till time
# 	# simFuc is the simulation function
# 	# which takes label, initial condition and simulation time
# 	retval = defaultdict(list)
# 	numVertex = g.vcount()
# 	initValues = [[] for _ in range(numVertex)]
# 	timeConcat = [[] for _ in range(numVertex)]
	
# 	initValues[0].append(initialSet)
# 	timeConcat[0].append((0,0))

# 	computerOrder = g.topological_sorting(mode=OUT)
# 	vertexOrder = 0
# 	remainTime = timeHorizon
# 	breakflag = False
# 	modeSwitchDic = {}
# 	reachtubeResult = []

# 	while remainTime > 0:
# 		curVertex = computerOrder[vertexOrder]
# 		curSuccessors = g.successors(curVertex)
# 		curPredecessors = g.predecessors(curVertex)

# 		if DEBUG:
# 			print NEWLINE
# 			print("Current State is the %d th mode with name %s" %(curVertex, g.vs[curVertex]["name"]))

# 		for s in curSuccessors:
# 			modeSwitchDic[s] = str(curVertex)+'->'+str(s)
# 		if len(curPredecessors) == 0:
# 			modeSwitchDic[curVertex] = str(curVertex)

# 		# Determine the time that we stay in this mode
# 		if len(curSuccessors) == 0:
# 			# If there is no successor, stay the remain time
# 			transiteTimeMax = float(remainTime)
# 			if vertexOrder == len(computerOrder)-1:
# 				breakflag = True
# 		else:
# 			# If there are successors, find the max time we can stay in this mode
# 			transiteTimeMax = float('-inf')

# 			for curSuc in curSuccessors:
# 				edgeID = g.get_eid(curVertex, curSuc)
# 				curTransitTime = g.es[edgeID]['trans_time']
# 				g.vs[curSuc]['remainTime'] = max(
# 					g.vs[curSuc]['remainTime'],
# 					g.vs[curVertex]['remainTime']-curTransitTime[0]
# 				)
# 				transiteTimeMax = max(transiteTimeMax, curTransitTime[1])

# 			transiteTimeMax = float(min(transiteTimeMax), remainTime)

# 		reachtubeResult.append(' %'+g.vs[curVertex]['name']+' '+modeSwitchDic[curVertex]+'\n')

# 		for idx, initialSet in enumerate(initValues[curVertex]):
# 			# Loop through all the initial sets we have for this mode
# 			# This is because mutiple previous mode can go to current mode
# 			curDelta = calcDelta(initialSet[0], initialSet[1])
# 			if DEBUG:
# 				print "Initial Condition is", initialSet
# 				print "Initial Delta is ", curDelta
# 				print "Time used to concat is ", timeConcat[curVertex][idx]

			
