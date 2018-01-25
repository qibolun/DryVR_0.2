from examples import c2e2wrapper
import math

def TC_Simulate(Mode,initialCondition,time_bound):
    # Map givien mode to int 1
    modes = "Rampup_A, Rampup_B, Rampup_C, Rampup_D, Rampup_E, Rampup_F, Rampup_G, On_A, On_B, On_C, On_D, On_E, On_F, On_G, Rampdown_A, Rampdown_B, Rampdown_C, Rampdown_D, Rampdown_E, Rampdown_F, Rampdown_G, Off_A, Off_B, Off_C, Off_D, Off_E, Off_F, Off_G"
    modes = modes.split(',')
    allmodes = []
    for mode in modes:
        allmodes.append(mode.strip())
    modenum = allmodes.index(Mode)+1

    simfile = './examples/hybrid_inverter_ramp/simu'
    timeStep = 0.00002
    # This model need some spcial handle 
    # This is because we want to discard the t in the simulator
    # Adding t to the simulation initial condition
    initialCondition = [initialCondition[0], 0.0 ,initialCondition[1]]
    result = c2e2wrapper.invokeSimulator(
        modenum,
        simfile,
        initialCondition,
        timeStep,
        time_bound
    )

    ret = []
    # Discard time info from the simulator and return to DRYVR

    def checkinvalidnum(val):
        # Avoid simulator out of boundary
        if math.isnan(val):
            return True

        if val == float('inf') or val == float('-inf'):
            return True

        # The value cannot be larger than 10 or less than -10
        if val > 10 or val <-10:
            return True

        return False


    for line in result:
        if checkinvalidnum(line[1]):
            break
        ret.append([line[0], line[1], line[3]])

    print ret[-1]
    return ret


if __name__ == "__main__":
    TC_Simulate("Rampup_A",1,1)
