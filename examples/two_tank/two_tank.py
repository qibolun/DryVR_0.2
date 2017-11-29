from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def two_tank_dynamic(y, t, Mode):
    x1, x2 = y
    x1 = float(x1)
    x2 = float(x2)

    if Mode == "off_off":
        x1_dot = -x1 - 2
        x2_dot = x1
    elif Mode == "off_on":
        x1_dot = -x1 - 2
        x2_dot = x1 - x2 - 5
    elif Mode == "on_off":
        x1_dot = -x1 + 3
        x2_dot = x1
    elif Mode == "on_on":
        x1_dot = -x1 + 3
        x2_dot = x1 - x2 - 5

    dydt = [x1_dot, x2_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.01;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(two_tank_dynamic,initialCondition,t, args=(Mode,),hmax = time_step)

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
    sol = TC_Simulate('on_on',[2.5,1.0],5)

    time = [row[0] for row in sol]

    a = [row[1] for row in sol]

    b = [row[2] for row in sol]

    plt.plot(time, a, "-r")
    plt.plot(time, b, "-g")
    plt.show()
    plt.plot(a, b, "-r")
    plt.show()
