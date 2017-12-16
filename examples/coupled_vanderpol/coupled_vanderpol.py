from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/spring-pendulum/

def couple_vanderpol_dynamic(y,t):
    x1,y1,x2,y2 = y
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)

    x1_dot = y1
    y1_dot = (1 - x1**2)*y1 - x1 + (x2 - x1)
    x2_dot = y2
    y2_dot = (1 - x2**2)*y2 - x2 + (x1 - x2)

    dydt = [x1_dot, y1_dot, x2_dot, y2_dot]
    return dydt

def TC_Simulate(Mode, initialCondition, time_bound):
    time_step = 0.05;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(couple_vanderpol_dynamic, initialCondition, t, hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        tmp.append(float(sol[j,2]))
        tmp.append(float(sol[j,3]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("Default", [1.25, 2.25, 1.25, 2.25], 7.0)
    #for s in sol:
	#	print(s)

    time = [row[0] for row in sol]

    a = [row[1] for row in sol]

    b = [row[2] for row in sol]

    c = [row[3] for row in sol]

    d = [row[4] for row in sol]

    # plt.plot(time, a, "-r")
    # plt.plot(time, b, "-g")
    # plt.show()
    plt.plot(a, b, "-r")
    plt.show()