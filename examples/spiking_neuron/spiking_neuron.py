from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/spiking-neurons/

def spiking_neuron_dynamic(y,t):
    v, u = y
    v = float(v)
    u = float(u)

    C = 100
    v_r = -56
    v_t = -42
    I = 300
    a = 0.03
    b = 8
    k = 1

    v_dot = (k * (v - v_r) * (v - v_t) - u + I)/C
    u_dot = a * (b * (v - v_r) - u)

    dydt = [v_dot, u_dot]

    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.1;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(spiking_neuron_dynamic, initialCondition, t, hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):

        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        trace.append(tmp)
    return trace
    
if __name__ == "__main__":

    sol = TC_Simulate("Default", [-50, 0.0], 10.0)
    #for s in sol:
	#	print(s)

    time = [row[0] for row in sol]

    a = [row[1] for row in sol]

    b = [row[2] for row in sol]

    plt.plot(time, a, "-r")
    plt.plot(time, b, "-g")
    plt.show()
    plt.plot(a, b, "-r")
    plt.show()

