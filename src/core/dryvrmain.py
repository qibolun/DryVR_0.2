"""
This file contains a single function that verifies model
"""
import random
import time

import src.common.config as userConfig
from src.common.constant import *
from src.common.io import parseVerificationInputFile, writeReachTubeFile, parseRrtInputFile, writeRrtResultFile
from src.common.utils import importSimFunction, randomPoint, buildModeStr, isIpynb, overloadConfig
from src.core.distance import DistChecker
from src.core.dryvrcore import *
from src.core.goalchecker import GoalChecker
from src.core.graph import Graph
from src.core.guard import Guard
from src.core.initialset import InitialSet
from src.core.initialsetstack import InitialSetStack, GraphSearchNode
from src.core.reset import Reset
from src.core.reachtube import ReachTube
from src.core.uniformchecker import UniformChecker

def verify(data, simFunction, paramConfig={}):
    """
    DryVR verification algorithm.
    It does the verification and print out the verify result.
    
    Args:
        data (dict): dictionary that contains params for the input file
        simFunction (function): black-box simulation function
        paramConfig (dict): user-specified configuration

    Returns:
        Safety (str): safety of the system
        Reach (obj): reach tube object

    """
    # There are some fields can be config by user,
    # If user specified these fields in paramConfig, 
    # overload these parameters to userConfig
    overloadConfig(userConfig, paramConfig)

    GLOBALREFINECOUNTER = 0

    params = parseVerificationInputFile(data)
    # Build the graph object
    graph = buildGraph(
        params.vertex,
        params.edge,
        params.guards,
        params.resets
    )

    # Build the progress graph for jupyter notebook
    # isIpynb is used to detect if the code is running
    # on notebook or terminal, the graph will only be shown
    # in notebook mode
    progressGraph = Graph(params, isIpynb())

    # Make sure the initial mode is specfieid if the graph is dag
    # FIXME should move this part to input check
    # Bolun 02/12/2018
    assert graph.is_dag()==True or params.initialVertex!=-1, "Graph is not DAG and you do not have initial mode!"

    checker = UniformChecker(params.unsafeSet, params.variables)
    guard = Guard(params.variables)
    reseter = Reset(params.variables)
    startTime = time.time()

    # Step 1) Simulation Test
    # Random generate points, then simulate and check the result
    for _ in range(userConfig.SIMUTESTNUM):
        randInit = randomPoint(params.initialSet[0], params.initialSet[1])

        if DEBUG:
            print 'Random checking round ', _, 'at point ', randInit

        # Do a full hybrid simulation
        simResult = simulate(
            graph,
            randInit,
            params.timeHorizon,
            guard,
            simFunction,
            reseter,
            params.initialVertex,
            params.deterministic
        )

        # Check the traces for each mode
        for mode in simResult:
            safety = checker.checkSimuTrace(simResult[mode], mode)
            if safety == -1:
                print 'Current simulation is not safe. Program halt'
                print 'simulation time', time.time()-startTime
                return "UNSAFE", None
    simEndTime = time.time()

    # Step 2) Check Reach Tube
    # Calculate the over approximation of the reach tube and check the result
    print "Verification Begin"

    # Get the initial mode
    if params.initialVertex == -1:
        computeOrder =  graph.topological_sorting(mode=OUT)
        initialVertex = computeOrder[0]
    else:
        initialVertex = params.initialVertex

    # Build the initial set stack
    curModeStack = InitialSetStack(initialVertex, userConfig.REFINETHRES, params.timeHorizon)
    curModeStack.stack.append(InitialSet(params.initialSet[0], params.initialSet[1]))
    curModeStack.bloatedTube.append(buildModeStr(graph, initialVertex))
    while True:
        # backwardFlag can be SAFE, UNSAFE or UNKNOWN
        # If the backwardFlag is SAFE/UNSAFE, means that the children nodes
        # of current nodes are all SAFE/UNSAFE. If one of the child node is
        # UNKNOWN, then the backwardFlag is UNKNOWN.
        backwardFlag = SAFE

        while curModeStack.stack:
            print str(curModeStack)
            print curModeStack.stack[-1]

            if not curModeStack.isValid():
                # A stack will be invalid if number of initial sets 
                # is more than refine threshold we set for each stack.
                # Thus we declare this stack is UNKNOWN
                print curModeStack.mode, "is not valid anymore"
                backwardFlag = UNKNOWN
                break

            # This is condition check to make sure the reach tube output file 
            # will be readable. Let me try to explain this.
            # A reachtube outout will be something like following
            # MODEA->MODEB
            # [0.0, 1.0, 1.1]
            # [0.1, 1.1, 1.2]
            # .....
            # Once we have refinement, we will add mutiple reach tube to 
            # this curModeStack.bloatedTube
            # However, we want to copy MODEA->MODEB so we know thats two different
            # reach tube from two different refined initial set
            # The result will be look like following
            # MODEA->MODEB
            # [0.0, 1.0, 1.1]
            # [0.1, 1.1, 1.2]
            # .....
            # MODEA->MODEB (this one gets copied!)
            # [0.0, 1.5, 1.6]
            # [0.1, 1.6, 1.7]
            # .....
            if isinstance(curModeStack.bloatedTube[-1], list):
                curModeStack.bloatedTube.append(curModeStack.bloatedTube[0])


            curStack = curModeStack.stack
            curVertex = curModeStack.mode
            curRemainTime = curModeStack.remainTime
            curLabel = graph.vs[curVertex]['label']
            curSuccessors = graph.successors(curVertex)
            curInitial = [curStack[-1].lowerBound, curStack[-1].upperBound]
            # Update the progress graph
            progressGraph.update(buildModeStr(graph, curVertex), curModeStack.bloatedTube[0], curModeStack.remainTime)

            if len(curSuccessors) == 0:
                # If there is not successor
                # Calculate the current bloated tube without considering the guard
                curBloatedTube = clacBloatedTube(curLabel,
                    curInitial,
                    curRemainTime,
                    simFunction,
                    params.bloatingMethod,
                    params.kvalue,
                    userConfig.SIMTRACENUM,
                )

            candidateTube = []
            shortestTime = float("inf")
            shortestTube = None

            for curSuccessor in curSuccessors:
                edgeID = graph.get_eid(curVertex, curSuccessor)
                curGuardStr = graph.es[edgeID]['guards']
                curResetStr = graph.es[edgeID]['resets']
                # Calulcate the current bloated tube with guard involved
                # Pre-check the simulation trace so we can get better bloated result
                curBloatedTube = clacBloatedTube(curLabel,
                    curInitial,
                    curRemainTime,
                    simFunction,
                    params.bloatingMethod,
                    params.kvalue,
                    userConfig.SIMTRACENUM,
                    guardChecker = guard,
                    guardStr = curGuardStr,
                )

                # Use the guard to calculate the next initial set
                nextInit, trunckedResult, transiteTime = guard.guardReachTube(
                    curBloatedTube,
                    curGuardStr,
                )

                
                if nextInit == None:
                    continue

                # Reset the next initial set
                nextInit = reseter.resetSet(curResetStr, nextInit[0], nextInit[1])

                # Build next mode stack
                nextModeStack = InitialSetStack(
                    curSuccessor,
                    userConfig.CHILDREFINETHRES,
                    curRemainTime-transiteTime,
                )
                nextModeStack.parent = curModeStack
                nextModeStack.stack.append(InitialSet(nextInit[0], nextInit[1]))
                nextModeStack.bloatedTube.append(curModeStack.bloatedTube[0]+'->'+buildModeStr(graph, curSuccessor))
                curStack[-1].child[curSuccessor] = nextModeStack
                if len(trunckedResult)>len(candidateTube):
                    candidateTube = trunckedResult

                # In case of must transition
                # We need to record shortest tube
                # As shortest tube is the tube invoke transition
                if trunckedResult[-1][0] < shortestTime:
                    shortestTime = trunckedResult[-1][0]
                    shortestTube = trunckedResult

            # Handle must transition
            if params.deterministic and len(curStack[-1].child)>0:
                nextModesInfo = []
                for nextMode in curStack[-1].child:
                    nextModesInfo.append((curStack[-1].child[nextMode].remainTime, nextMode))
                # This mode gets transit first, only keep this mode
                maxRemainTime, maxTimeMode = max(nextModesInfo)
                # Pop other modes becuase of deterministic system
                for _, nextMode in nextModesInfo:
                    if nextMode == maxTimeMode:
                        continue
                    curStack[-1].child.pop(nextMode)
                candidateTube = shortestTube
                print "Handle deterministic system, next mode", graph.vs[curStack[-1].child.keys()[0]]['label']

            if not candidateTube:
                candidateTube = curBloatedTube

            # Check the safety for current bloated tube
            safety = checker.checkReachTube(candidateTube, curLabel)
            if safety == UNSAFE:
                print "System is not safe in Mode ", curLabel
                # Start back Tracking from this point and print tube to a file
                # push current unsafeTube to unsafe tube holder
                unsafeTube = [curModeStack.bloatedTube[0]] + candidateTube
                while curModeStack.parent is not None:
                    prevModeStack = curModeStack.parent
                    unsafeTube = [prevModeStack.bloatedTube[0]] + prevModeStack.stack[-1].bloatedTube + unsafeTube
                    curModeStack = prevModeStack
                print 'simulation time', simEndTime-startTime
                print 'verification time', time.time()-simEndTime
                print 'refine time', GLOBALREFINECOUNTER
                writeReachTubeFile(unsafeTube, UNSAFEFILENAME)
                retReach = ReachTube(curModeStack.bloatedTube, params.variables, params.vertex)
                return "UNSAFE", retReach

            elif safety == UNKNOWN:
                # Refine the current initial set
                print curModeStack.mode, "check bloated tube unknown"
                discardInitial = curModeStack.stack.pop()
                initOne, initTwo = discardInitial.refine()
                curModeStack.stack.append(initOne)
                curModeStack.stack.append(initTwo)
                GLOBALREFINECOUNTER+=1

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
                    print "No child exist in current initial, pop"

        if curModeStack.parent is None:
            # We are at head now
            if backwardFlag == SAFE:
                # All the nodes are safe
                print "System is Safe!"
                print "refine time", GLOBALREFINECOUNTER
                writeReachTubeFile(curModeStack.bloatedTube, REACHTUBEOUTPUT)
                retReach = ReachTube(curModeStack.bloatedTube, params.variables, params.vertex)
                print 'simulation time', simEndTime-startTime
                print 'verification time', time.time()-simEndTime
                return "SAFE", retReach
            elif backwardFlag == UNKNOWN:
                print "Hit refine threshold, system halt, result unknown"
                print 'simulation time', simEndTime-startTime
                print 'verification time', time.time()-simEndTime
                return "UNKNOWN", None
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
                GLOBALREFINECOUNTER+=1


def graphSearch(data, simFunction, paramConfig={}):
    """
    DryVR controller synthesis algorithm.
    It does the controller synthesis and print out the search result.
    tube and transition graph will be stored in ouput folder if algorithm finds one
    
    Args:
        data (dict): dictionary that contains params for the input file
        simFunction (function): black-box simulation function

    Returns:
        None

    """
    # There are some fields can be config by user,
    # If user specified these fields in paramConfig, 
    # overload these parameters to userConfig
    overloadConfig(userConfig, paramConfig)
    # Parse the input json file and read out the parameters
    params = parseRrtInputFile(data)
    # Construct objects
    checker = UniformChecker(params.unsafeSet, params.variables)
    goalSetChecker = GoalChecker(params.goalSet, params.variables)
    distanceChecker = DistChecker(params.goal, params.variables)
    # Read the important param
    availableModes = params.modes
    startModes = params.modes
    remainTime = params.timeHorizon
    minTimeThres = params.minTimeThres

    # Set goal rach flag to False
    # Once the flag is set to True, It means we find a transition Graph
    goalReached = False

    # Build the initial mode stack
    # Current Method is ugly, we need to get rid of the initial Mode for GraphSearch
    # It helps us to achieve the full automate search
    # TODO Get rid of the initial Mode thing
    random.shuffle(startModes)
    dummyNode = GraphSearchNode("start", remainTime, minTimeThres, 0)
    for mode in startModes:
        dummyNode.children[mode] = GraphSearchNode(mode, remainTime, minTimeThres, dummyNode.level+1)
        dummyNode.children[mode].parent = dummyNode
        dummyNode.children[mode].initial = (params.initialSet[0], params.initialSet[1])

    curModeStack = dummyNode.children[startModes[0]]
    dummyNode.visited.add(startModes[0])
    
    startTime = time.time()
    while True:

        if not curModeStack:
            break

        if curModeStack == dummyNode:
            startModes.pop(0)
            if len(startModes)==0:
                break
            
            
            curModeStack = dummyNode.children[startModes[0]]
            dummyNode.visited.add(startModes[0])
            continue
        
        print str(curModeStack)

        # Keep check the remain time, if the remain time is less than minTime
        # It means it is impossible to stay in one mode more than minTime
        # Therefore, we have to go back to parents
        if curModeStack.remainTime < minTimeThres:
            print "Back to previous mode because we cannot stay longer than the min time thres"
            curModeStack = curModeStack.parent
            continue

        # If we have visited all available modes
        # We should select a new candidate point to proceed
        # If there is no candidates available,
        # Then we can say current node is not valid and go back to parent
        if len(curModeStack.visited) == len(availableModes):
            if len(curModeStack.candidates)<2:
                print "Back to previous mode because we do not have any other modes to pick"
                curModeStack = curModeStack.parent
                # If the tried all possible cases with no luck to find path
                if not curModeStack:
                    break
                continue
            else:
                print "Pick a new point from candidates"
                curModeStack.candidates.pop(0)
                curModeStack.visited = set()
                curModeStack.children = {}
                continue


        # Generate bloated tube if we haven't done so
        if not curModeStack.bloatedTube:
            print "no bloated tube find in this mode, generate one"
            curBloatedTube = clacBloatedTube(
                curModeStack.mode,
                curModeStack.initial,
                curModeStack.remainTime,
                simFunction,
                params.bloatingMethod,
                params.kvalue,
                userConfig.SIMTRACENUM
            )

            # Cut the bloated tube once it intersect with the unsafe set
            curBloatedTube = checker.cutTubeTillUnsafe(curBloatedTube)

            # If the tube time horizon is less than minTime, it means
            # we cannot stay in this mode for min thres time, back to the parent node
            if not curBloatedTube or curBloatedTube[-1][0] < minTimeThres:
                print "bloated tube is not long enough, discard the mode"
                curModeStack = curModeStack.parent
                continue
            curModeStack.bloatedTube = curBloatedTube

            # Generate candidates points for next node
            randomSections = curModeStack.randomPicker(userConfig.RANDSECTIONNUM)

            if not randomSections:
                print "bloated tube is not long enough, discard the mode"
                curModeStack = curModeStack.parent
                continue

            # Sort random points based on the distance to the goal set
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
        # This is actually not necssary, just shuffle all modes would be enough
        # There should not be RANDMODENUM things since it does not make any difference
        # Anyway, for each candidate point, we will try to visit all modes eventually
        # Therefore, using RANDMODENUM to get some random modes visit first is useless
        # TODO, fix this part
        if len(curModeStack.visited) == len(curModeStack.children):
            # leftMode = set(availableModes) - set(curModeStack.children.keys())
            # randomModes = random.sample(leftMode, min(len(leftMode), RANDMODENUM))
            # random.shuffle(randomModes)
            randomModes = availableModes
            random.shuffle(randomModes)

            randomSections = curModeStack.randomPicker(userConfig.RANDSECTIONNUM)
            for mode in randomModes:
                candidate = curModeStack.candidates[0]
                curModeStack.children[mode] = GraphSearchNode(mode, curModeStack.remainTime-candidate[1][0], minTimeThres, curModeStack.level+1)
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
    print "RRT run time", time.time()-startTime
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
            if curModeStack.parent != dummyNode:
                curModeStack = curModeStack.parent
            else:
                break
        # Reorganize the content in modes list for plotter use
        modes = modes[::-1]
        traces = traces[::-1]
        buildRrtGraph(modes, traces, isIpynb())
        for i in range(1, len(modes)):
            modes[i] = modes[i-1]+'->'+modes[i]

        writeRrtResultFile(modes, traces, RRTOUTPUT)
    else:
        print("could not find graph")
