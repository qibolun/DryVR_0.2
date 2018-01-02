from examples import c2e2wrapper

def TC_Simulate(Mode,initialCondition,time_bound):
    # Map givien mode to int 1
    if Mode == "OR_Rampup":
        modenum = 1
    elif Mode == "OR_On":
        modenum = 2
    elif Mode == "OR_Rampdown":
        modenum = 3
    elif Mode == "OR_Off":
        modenum = 4
	
    simfile = './examples/uniform_NOR_ramp/simu'
    timeStep = 0.00002
    # This model need some spcial handle 
    # This is because we want to discard the t in the simulator
    # Adding t to the simulation initial condition
    initialCondition = [initialCondition[0], initialCondition[1], initialCondition[2], 0.0 ,initialCondition[3]]
    result = c2e2wrapper.invokeSimulator(
        modenum,
        simfile,
        initialCondition,
        timeStep,
        time_bound
    )

    ret = []
    # Discard time info from the simulator and return to DRYVR
    for line in result:
        ret.append([line[0], line[1], line[2], line[3], line[5]])
    
    return ret
