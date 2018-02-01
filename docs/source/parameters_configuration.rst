.. _parameter-label:

Parameters configuration
===============================

Parameters in DryVR can be changed by user to get desire result for verification and synthesis.
The configuration file is stored in ::

	src/common/constant.py

The following parameters can be changed user ::

	# Verification constant
	SIMUTESTNUM = 1
	SIMTRACENUM = 10
	REFINETHRES = 10
	CHILDREFINETHRES = 2

	# Synthesis Constant
	RANDMODENUM = 3
	RANDSECTIONNUM = 3


Verification constant:
- SIMUTESTNUM is the number of hybrid simulation runs at beginning of the verification algorithm to find counter examples.

- SIMTRACENUM is number of sumulation traces generated to learn the sensitity (discrepancy function).

- REFINETHRES is the refine threshold for initial set given by user.

- CHILDREFINETHRES is the refine threshold for child node initial set. When DryVR runs verification algorithm, it uses DFS algorithm to go through the transition graph, and generate a child node for vertex in graph, this threshold is for child node.


Synthesis Constant:

- RANDMODENUM is the number of random modes picked to precced synthesis algorithm

- RANDSECTIONNUM is number of time intervals picked as next set of candidate guards


