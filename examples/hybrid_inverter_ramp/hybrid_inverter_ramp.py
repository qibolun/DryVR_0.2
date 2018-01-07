from examples import c2e2wrapper

def TC_Simulate(Mode,initialCondition,time_bound):
    # Map givien mode to int 1
    if Mode == "Rampup_A":
        modenum = 1
    elif Mode == "Rampup_B":
        modenum = 2
    elif Mode == "Rampup_C":
        modenum = 3
    elif Mode == "Rampup_D":
        modenum = 4
    elif Mode == "Rampup_E":
        modenum = 5
    elif Mode == "Rampup_F":
        modenum = 6
    elif Mode == "Rampup_G":
        modenum = 7
    elif Mode == "On_A":
        modenum = 8
    elif Mode == "On_B":
        modenum = 9
    elif Mode == "On_C":
        modenum = 10
    elif Mode == "On_D":
        modenum = 11
    elif Mode == "On_E":
        modenum = 12
    elif Mode == "On_F":
        modenum = 13
    elif Mode == "On_G":
        modenum = 14
    elif Mode == "Rampdown_A":
        modenum = 15
    elif Mode == "Rampdown_B":
        modenum = 16
    elif Mode == "Rampdown_C":
        modenum = 17
    elif Mode == "Rampdown_D":
        modenum = 18
    elif Mode == "Rampdown_E":
        modenum = 19
    elif Mode == "Rampdown_F":
        modenum = 20
    elif Mode == "Rampdown_G":
        modenum = 21
    elif Mode == "Off_A":
        modenum = 22
    elif Mode == "Off_B":
        modenum = 23
    elif Mode == "Off_C":
        modenum = 24
    elif Mode == "Off_D":
        modenum = 25
    elif Mode == "Off_E":
        modenum = 26
    elif Mode == "Off_F":
        modenum = 27
    elif Mode == "Off_G":
        modenum = 28

    simfile = './examples/uniform_NOR_sigmoid/simu'
    timeStep = 0.00005
    # This model need some spcial handle 
    # This is because we want to discard the t in the simulator
    # Adding t to the simulation initial condition
    initialCondition = [ initialCondition[0], 0.0, initialCondition[1]]
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
        ret.append([line[0], line[1], line[3])
    
    return ret
