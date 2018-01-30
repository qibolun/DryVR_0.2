from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def PDE_dynamics(y,t,u1):
    x1, x2, x3, x4, x5, x6 = y
    x1 = float(x1)
    x2 = float(x2)
    x3 = float(x3)
    x4 = float(x4)
    x5 = float(x5)
    x6 = float(x6)

    x1_dot = 4.213*x3 - 252.57*x1 - 106.6*x2 - 51.94*u1 + 13.09*x4 - 1.8157*x5 + 0.4038*x6
    x2_dot = 63.509*x3 - 106.6*x1 - 777.63*x2 - 11.124*u1 + 184.91*x4 - 26.094*x5 + 5.8051*x6
    x3_dot = 21.751*x5 - 4.213*x1 - 63.509*x2 - 25.034*x3 - 251.84*x4 - 0.43288*u1 - 4.797*x6
    x4_dot = 1.3463*u1 + 13.09*x1 + 184.91*x2 + 251.84*x3 - 634.37*x4 + 172.68*x5 - 39.239*x6
    x5_dot = 172.68*x4 - 1.8157*x1 - 26.094*x2 - 21.751*x3 - 0.1867*u1 - 645.44*x5 + 337.53*x6
    x6_dot = 39.239*x4 - 0.4038*x1 - 5.8051*x2 - 4.797*x3 - 0.041519*u1 - 337.53*x5 - 213.54*x6

    dydt = [x1_dot, x2_dot, x3_dot, x4_dot, x5_dot, x6_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.005;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.3f')))
    t = newt

    u1 = 0.75

    sol = odeint(PDE_dynamics, initialCondition, t, args=(u1,), hmax=time_step)

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
        trace.append(tmp)
    return trace

if __name__ == "__main__":
    sol = TC_Simulate("Default", [-0.002, -0.0004, -0.001, -0.0019, -0.0008, -0.0001, 0.1, 1.0], 20.0)
    #for s in sol:
	#	print(s)

    time = [row[0] for row in sol]

    a = [row[1] for row in sol]

    plt.plot(time, a, "-r")
    plt.show()
    plt.show()
