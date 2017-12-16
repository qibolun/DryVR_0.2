from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Souce: https://ths.rwth-aachen.de/research/projects/hypro/lorentz-system/ 

def lorentz_dynamic(y,t):
    a, b, c = y
    a = float(a)
    b = float(b)
    c = float(c)

    a_dot = 10.0*(b-a)
    b_dot = a*(28.0 - c) - b
    c_dot = a*b - 8.0/3*c

    dydt = [a_dot, b_dot, c_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.003;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(lorentz_dynamic, initialCondition, t, hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        tmp.append(float(sol[j,2]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("Default", [15.0, 15.0, 36.0], 10.0)
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

