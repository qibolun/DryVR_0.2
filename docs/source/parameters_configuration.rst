.. _parameter-label:

Parameters configuration
===============================

Parameters in DryVR can be changed by users to get desire result for verification and synthesis.
The configuration file is stored in ::

	src/common/constant.py

The following parameters can be changed by users ::

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

- SIMTRACENUM is the number of sumulation traces generated to learn the sensitity (discrepancy function).

- REFINETHRES is the refine threshold for initial set given by user.

- CHILDREFINETHRES is threshold of the refinement times for non-initial vertices of the transition graph


Synthesis Constant:

- RANDMODENUM is the number of random modes picked at each time for each candidate guard

- RANDSECTIONNUM is number of time intervals picked as the next set of candidate guards


