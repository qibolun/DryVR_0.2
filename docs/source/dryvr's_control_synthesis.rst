DryVR's Synthesis Language
=================================

In DryVR,  a hybrid system is modeled as a combination of a white-box that specifies the mode switches (:ref:`transition-graph-label`) and a black-box that can simulate the continuous evolution in each mode (:ref:`black-box-label`).

The control synthesis problem for DryVR is to find a white-box transition graph given the black-box simulator with addition inputs listed in (:ref:`input-format-control-label`). 

.. _input-format-control-label:

Input Format
^^^^^^^^^^^^^^^^^^^^^^^^^

The input for DryVR control synthesis is of the form ::

    {
      "modes":[modes that black simulator takes]
      "variables":[the name of variables in the system]
      "initialSet":[two arrays defining the lower and upper bound of each variable]
      "unsafeSet":@[mode name]:[unsafe region]
      "goalSet":[A z3 expression for target set]
      "timeHorizon":[time bound for control synthesis, the graph should be bounded in time horizon]
      "directory": directory of the folder which contains the simulator for black-box system
      "minTimeThres": minimal staying time for each mode to limit number of trainsition.
      "goal":[[goal variables],[lower bound][upper bound]] # This is a rewrite for goal set for dryvr to calculate distance.
    }

Example input for the robot in maze example ::

    {
      "modes":["0", "1", "2", "3", "4", "5", "6", "7"],
      "variables":["x","y","vx","vy"],
      "initialSet":[[1.0,1.0,1.0,1.0],[1.1,1.0,1.0,1.0]],
      "unsafeSet":"@Allmode:Or(And(x>=2.0, x<3.0, y>=3.0, y<=4.0), And(x>=3.0, x<=4.0, y>=2.0, y<3.0), x<0, x>5, y<0, y>5)",
      "goalSet":"And(x>=3.0, x<=4.0, y>=3.0, y<=4.0)",
      "timeHorizon":10.0,
      "minTimeThres":1.0,
      "directory":"examples/carinmaze",
      "goal":[["x","y"],[3.0,3.0],[4.0,4.0]]
    }


Output Interpretation
^^^^^^^^^^^^^^^^^^^^^^^^^

The tool will print background information like the current mode, transition time, initial set on the run. The final result about goal reached or not reached will be printed at the bottom.

When the system find the transition graph that statisfy the requirement, the final result will look like ::

    goal reached

When the system cannot find graph, the final result will look like ::

    could not find graph

Note that DryVR's algorithm is searching the graph randomly, if the system cannot find the graph, it does not mean the graph is not exist with current input. You can try run the algorithm multiple times to get more accurate result. Increase RANDSECTIONNUM in DryVR's configuration will increase the chance of finding hte transition graph. (See {:ref:`parameter-label`}) 
If the the system find the transition graph, the system will plot the transition graph and will be stored in "output/rrtGraph.png"

Advanced Tricks: Making control synthesis work on your own black-box system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating black box simulator is exactly same as we introduced in DryVR's language page (:ref:`advance-label`) up to Step 4.

For the Step 5, instead of creating a verification input file, you need to create control synthesis input file we have discussed in :ref:`input-format-control-label`.

For example, Let's set the intial temperature within the range :math:`[75,76]`, and we want to reach the target temperature within the range :math:`[68,72]`, while avoiding temperature that is larger than :math:`90`. We want to start our search from "On" mode and reach our goal in bounded time :math:`4s`, and set the minimal staying time to :math:`1s`. 

the input file can be written as: ::

    {	
      "modes":["On", "Off"],
      "initialMode":"On",
      "variables":["temp"],
      "initialSet":[[75.0],[76.0]],
      "unsafeSet":"@Allmode:temp>90",
      "goalSet":"And(temp>=68.0, temp<=72.0)",
      "timeHorizon":4.0,
      "minTimeThres":1.0,
      "directory":"examples/Thermostats",
      "goal":[["temp"],[68.0],[72.0]]
    }

Save the input file in the folder input/rrtinput and name it as temp.json.

Run the graph search algorithm using the command: ::

    python rrt.py input/rrtinput/temp.json

The graph has been found with the output: ::

    goal reached!

If you check the the output/rrtGraph.png, you would get a transition graph for this problem. As you can see the system turn from On state to Off state to reach the goal.

.. figure:: rrtGraph.png
    :scale: 60%
    :align: center
    :alt: thermostat transition graph

    The white box transition graph of the thermostat system







