from examples import c2e2wrapper

def TC_Simulate(Mode,initialCondition,time_bound):
	# Map givien mode to int 1
	modenum = 1
	simfile = './examples/uniform_inverter_loop/simu'
	timeStep = 0.0001
	result = c2e2wrapper.invokeSimulator(
		modenum,
		simfile,
		initialCondition,
		timeStep,
		time_bound
	)
	return result