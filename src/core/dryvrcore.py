"""
This file contains core functions used by DryVR
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy
import random

from collections import defaultdict
from igraph import *
from src.common.constant import *
from src.common.io import writeReachTubeFile
from src.common.utils import randomPoint,calcDelta,calcCenterPoint,buildModeStr,trimTraces
from src.discrepancy.Global_Disc import *
from src.discrepancy.PW_Discrepancy import PW_Bloat_to_tube

def buildGraph(vertex, edge, guards, resets):
    """
    Build graph object using given parameters
    
    Args:
        vertex (list): list of vertex with mode name
        edge (list): list of edge that connects vertex
        guards (list): list of guard corresponding to each edge
        resets (list): list of reset corresponding to each edge

    Returns:
        graph object

    """
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

def buildRrtGraph(modes, traces, isIpynb):
    """
    Build controller synthesis graph object using given modes and traces.
    Note this function is very different from buildGraph function.
    This is white-box transition graph learned from controller synthesis algorithm
    The reason to build it is to output the transition graph to file
    
    Args:
        modes (list): list of mode name
        traces (list): list of trace corresponding to each mode
        isIpynb (bool): check if it's in Ipython notebook environment

    Returns:
        None

    """
    if isIpynb:
        vertex = []
        # Build unique identifier for a vertex and mode name
        for idx,v in enumerate(modes):
            vertex.append(v+","+str(idx))

        edgeList = []
        edgeLabel = {}
        for i in range(1, len(modes)):
            edgeList.append((vertex[i-1],vertex[i]))
            lower = traces[i-1][-2][0]
            upper = traces[i-1][-1][0]
            edgeLabel[(vertex[i-1],vertex[i])] = "[" + str(lower) +"," + str(upper) + "]"

        fig = plt.figure()
        ax = fig.add_subplot(111)
        G = nx.DiGraph()
        G.add_edges_from(edgeList)
        pos = nx.spring_layout(G)
        colors = ['green'] * len(G.nodes())
        fig.suptitle('transition graph', fontsize=10)
        nx.draw_networkx_labels(G, pos)
        options = {
            'node_color': colors,
            'node_size': 1000,
            'cmap': plt.get_cmap('jet'),
            'arrowstyle': '-|>',
            'arrowsize': 50,
        }
        nx.draw_networkx(G, pos, arrows=True, **options)
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edgeLabel)
        fig.canvas.draw()
        


    else:
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


def simulate(g, initCondition, timeHorizon, guard, simFuc, reseter, initialVertex, deterministic):
    """
    This function does a full hybrid simulation

    Args:
        g (obj): graph object
        initCondition (list): initial point
        timeHorizon (float): time horizon to simulate
        guard (list): list of guard string corresponding to each transition
        simFuc (function): simulation function
        reseter (list): list of reset corresponding to each transition
        initialVertex (int): initial vertex that simulation starts
        deterministic (bool) : enable or disable must transition

    Returns:
        A dictionary obj contains simulation result.
        Key is mode name and value is the simulation trace.

    """

    retval = defaultdict(list)
    # If you do not delcare initialMode, then we will just use topological sort to find starting point
    if initialVertex == -1:
        computerOrder = g.topological_sorting(mode=OUT)
        curVertex = computerOrder[0]
    else:
        curVertex = initialVertex
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
            initCondition, trunckedResult = guard.guardSimuTrace(
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

                nextInit, trunckedResult = guard.guardSimuTrace(
                    curSimResult,
                    curGuardStr
                )

                nextInit = reseter.resetPoint(curResetStr, nextInit)
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

def clacBloatedTube(
        modeLabel, 
        initialSet, 
        timeHorizon, 
        simFuc, 
        bloatingMethod, 
        kvalue, 
        simTraceNum,
        guardChecker=None, 
        guardStr=None):
    """
    This function calculate the reach tube for single given mode

    Args:
        modeLabel (str): mode name
        initialSet (list): a list contains upper and lower bound of the initial set
        timeHorizon (float): time horizon to simulate
        simFuc (function): simulation function
        bloatingMethod (str): determine the bloating method for reach tube, either GLOBAL or PW
        simTraceNum (int): number of simulations used to calculate the discrepency
        kvalue (list): list of float used when bloating method set to PW
        guardChecker (obj): guard check object
        guardStr (str): guard string
       
    Returns:
        Bloated reach tube

    """
    curCenter = calcCenterPoint(initialSet[0], initialSet[1])
    curDelta = calcDelta(initialSet[0], initialSet[1])
    traces = []
    traces.append(simFuc(modeLabel, curCenter, timeHorizon))
    # Simulate SIMTRACENUM times to learn the sensitivity
    for _ in range(simTraceNum):
        newInitPoint = randomPoint(initialSet[0], initialSet[1])
        traces.append(simFuc(modeLabel, newInitPoint, timeHorizon))

    # Trim the trace to the same length
    traces = trimTraces(traces)
    if guardChecker is not None:
        # pre truncked traces to get better bloat result
        maxIdx = -1
        for trace in traces:
            retIdx = guardChecker.guardSimuTraceTime(trace, guardStr)
            maxIdx = max(maxIdx, retIdx+1)
        for i in range(len(traces)):
            traces[i] = traces[i][:maxIdx]

    if bloatingMethod == GLOBAL:
        if BLOATDEBUG:
            k, gamma = Global_Discrepancy(modeLabel, curDelta, 1, PLOTDIM, traces)
        else:
            k, gamma = Global_Discrepancy(modeLabel, curDelta, 0, PLOTDIM, traces)
        curReachTube = bloatToTube(modeLabel, k, gamma, curDelta, traces)
    elif bloatingMethod == PW:
        if BLOATDEBUG:
            curReachTube = PW_Bloat_to_tube(curDelta, 1, PLOTDIM, traces, kvalue)
        else:
            curReachTube = PW_Bloat_to_tube(curDelta, 0, PLOTDIM, traces, kvalue)
    return curReachTube
