from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def MCS_dynamic(y,t,u1,u2):
    x1, x2, x3, x4, x5, x6, x7, x8 = y
    x1 = float(x1)
    x2 = float(x2)
    x3 = float(x3)
    x4 = float(x4)
    x5 = float(x5)
    x6 = float(x6)
    x7 = float(x7)
    x8 = float(x8)

    x1_dot = x2
    x2_dot = 8487.17631024656293448060750961*x3 - 1.08651344319167389418907198612*x2
    x3_dot = -2592.1459854271597578190267086*x1 - 21.1189934732246911153197288513*x2 - 698.91348655731417238712310791*x3 - 141389.781024056253954768180847*x4
    x4_dot = x1 - 1.0*u1
    x5_dot = x6
    x6_dot = 8487.17631024656293448060750961*x7 - 1.08651344319167389418907198612*x6
    x7_dot = -2592.1459854271597578190267086*x5 - 21.1189934732246911153197288513*x6 - 698.91348655731417238712310791*x7 - 141389.781024056253954768180847*x8
    x8_dot = x5 - 1.0*u2

    dydt = [x1_dot, x2_dot, x3_dot, x4_dot, x5_dot, x6_dot, x7_dot, x8_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.001;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.3f')))
    t = newt

    u1 = 0.2
    u2 = 0.3

    sol = odeint(MCS_dynamic, initialCondition, t, args=(u1, u2), hmax = time_step)

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
        tmp.append(float(sol[j,4]))
        tmp.append(float(sol[j,5]))
        tmp.append(float(sol[j,6]))
        tmp.append(float(sol[j,7]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("Default", [0.002, 0.0, 0.0, 0.0, 0.001, 0.0, 0.0, 0.0, 0.002, 0.001, 0.16, 0.2], 20.0)
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
