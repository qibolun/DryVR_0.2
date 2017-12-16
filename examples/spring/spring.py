from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/spring-pendulum/ 

def spring_dynamic(y,t):
    r, theta, dr, dtheta = y
    r = float(r)
    theta = float(theta)
    dr = float(dr)
    dtheta = float(dtheta)


    r_dot = dr
    theta_dot = dtheta
    dr_dot = r*dtheta**2 + 9.8*np.cos(theta) - 2*(r - 1)
    dtheta_dot = (-2*dr*dtheta - 9.8*np.sin(theta))/r

    dydt = [r_dot, theta_dot, dr_dot, dtheta_dot]
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

    sol = odeint(spring_dynamic, initialCondition, t, hmax=time_step)

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

    sol = TC_Simulate("Default", [1.2, 0.5, 0.0, 0.0], 10.0)
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
    plt.plot(b, a, "-r")
    plt.show()
