from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def hybrid_inverter_ramp_dynamic(y,t,mode):
    v, stim_local = y
    v = float(v)
    stim_local = float(stim_local)

    if mode == "Rampup_A":
        # = 1
        stim_local_dot = 1
        v_dot = (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "Rampup_B":
        # = 1
        stim_local_dot = 1
        v_dot = (-stim_local + 0.4)*(2295.0*stim_local - 918.0) + (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "Rampup_C":
        # = 1
        stim_local_dot = 1
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "Rampup_D":
        # = 1
        stim_local_dot = 1
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435) - (stim_local - 0.4)*(2295.0*stim_local - 918.0)
    elif mode == "Rampup_E":
        # = 1
        stim_local_dot = 1
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4) + (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "Rampup_F":
        # = 1
        stim_local_dot = 1
        v_dot = (-2295.0*stim_local + 918.0)*(stim_local - 0.4)
    elif mode == "Rampup_G":
        # = 1
        stim_local_dot = 1
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4) 
    elif mode == "On_A":
        # = 1
        stim_local_dot = 0
        v_dot = (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "On_B":
        # = 1
        stim_local_dot = 0
        v_dot = (-stim_local + 0.4)*(2295.0*stim_local - 918.0) + (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "On_C":
        # = 1
        stim_local_dot = 0
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "On_D":
        # = 1
        stim_local_dot = 0
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435) - (stim_local - 0.4)*(2295.0*stim_local - 918.0)
    elif mode == "On_E":
        # = 1
        stim_local_dot = 0
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4) + (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "On_F":
        # = 1
        stim_local_dot = 0
        v_dot = (-2295.0*stim_local + 918.0)*(stim_local - 0.4)
    elif mode == "On_G":
        # = 1
        stim_local_dot = 0
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4)
    elif mode == "Rampdown_A":
        # = 1
        stim_local_dot = -1
        v_dot = (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "Rampdown_B":
        # = 1
        stim_local_dot = -1
        v_dot = (-stim_local + 0.4)*(2295.0*stim_local - 918.0) + (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "Rampdown_C":
        # = 1
        stim_local_dot = -1
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "Rampdown_D":
        # = 1
        stim_local_dot = -1
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435) - (stim_local - 0.4)*(2295.0*stim_local - 918.0)
    elif mode == "Rampdown_E":
        # = 1
        stim_local_dot = -1
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4) + (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "Rampdown_F":
        # = 1
        stim_local_dot = -1
        v_dot = (-2295.0*stim_local + 918.0)*(stim_local - 0.4)
    elif mode == "Rampdown_G":
        # = 1
        stim_local_dot = -1
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4)
    elif mode == "Off_A":
        # = 1
        stim_local_dot = -1
        v_dot = (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "Off_B":
        # = 1
        stim_local_dot = -1
        v_dot = (-stim_local + 0.4)*(2295.0*stim_local - 918.0) + (-5190.0*v + 6228.0)*(-stim_local + v/2 + 0.13)
    elif mode == "Off_C":
        # = 1
        stim_local_dot = -1
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "Off_D":
        # = 1
        stim_local_dot = -1
        v_dot = (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435) - (stim_local - 0.4)*(2295.0*stim_local - 918.0)
    elif mode == "Off_E":
        # = 1
        stim_local_dot = -1
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4) + (-1000000*stim_local + 730000.0)*(-0.002595*stim_local + 0.00189435)
    elif mode == "Off_F":
        # = 1
        stim_local_dot = -1
        v_dot = (-2295.0*stim_local + 918.0)*(stim_local - 0.4)
    elif mode == "Off_G":
        # = 1
        stim_local_dot = -1
        v_dot = -4590.0*v*(stim_local - v/2 - 0.4)

    dydt = [v_dot, stim_local_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.0005;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.6f')))
    t = newt
    # print t

    sol = odeint(hybrid_inverter_ramp_dynamic, initialCondition, t, args=(Mode,),hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("Rampup_A", [1.2,0.0], 6.4)
    #for s in sol:
	#	print(s)
    time = [row[0] for row in sol]

    v = [row[1] for row in sol]

    stim_local = [row[2] for row in sol]

    plt.plot(v,stim_local,"-r")
    plt.show()
    