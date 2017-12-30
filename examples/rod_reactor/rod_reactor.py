from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/rod-reactor/ 

def rod_reactor_dynamic(y,t,Mode):
    x, c1, c2 = y
    x = float(x)
    c1 = float(c1)
    c2 = float(c2)

    if Mode == "rod_1":
        x_dot = 0.1*x - 56
        c1_dot = 1
        c2_dot = 1
    elif Mode == "rod_2":
        x_dot = 0.1*x - 60
        c1_dot = 1
        c2_dot = 1
    elif Mode == "no_rod":
        x_dot = 0.1*x - 50
        c1_dot = 1
        c2_dot = 1

    dydt = [x_dot, c1_dot, c2_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
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

    sol = odeint(rod_reactor_dynamic,initialCondition,t, args=(Mode,),hmax = time_step)

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
    sol = TC_Simulate('rod_1',[510, 20, 20],50)

    time = [row[0] for row in sol]

    x = [row[1] for row in sol]

    c1 = [row[2] for row in sol]

    c2 = [row[3] for row in sol]

    plt.plot(x, c1, "-r")
    plt.show()
    plt.plot(x, c2, "-g")
    plt.show()
    plt.plot(c1, c2, "-r")
    plt.show()
