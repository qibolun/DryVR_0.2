from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def BM_dynamic(y,t,u1):
    x1, x2, x3, x4, x5, x6, y1 = y
    x1 = float(x1)
    x2 = float(x2)
    x3 = float(x3)
    x4 = float(x4)
    x5 = float(x5)
    x6 = float(x6)
    y1 = float(y1)

    x1_dot = 0.0061322*u1 - 0.0075102*x1 + 5.2756*x2 - 0.00096238*x3 - 0.6634*x4 - 0.006689*x5 + 0.16081*x6
    x2_dot = 0.064531*u1 - 5.2756*x1 - 0.85737*x2 + 0.090377*x3 + 0.92166*x4 + 0.13158*x5 - 0.97335*x6
    x3_dot = 0.00069603*u1 - 0.00096238*x1 - 0.090377*x2 - 0.00012541*x3 - 13.542*x4 - 0.00092367*x5 + 0.026749*x6
    x4_dot = 0.6634*x1 - 0.062226*u1 + 0.92166*x2 + 13.542*x3 - 1.004*x4 - 0.17895*x5 + 1.117*x6
    x5_dot = 0.0035048*u1 - 0.006689*x1 - 0.13158*x2 - 0.00092367*x3 + 0.17895*x4 - 0.008656*x5 + 23.761*x6
    x6_dot = 0.047228*u1 - 0.16081*x1 - 0.97335*x2 - 0.026749*x3 + 1.117*x4 - 23.761*x5 - 1.5873*x6
    y1 = 0.064531*x2 - 0.0061322*x1 - 0.00069603*x3 - 0.062226*x4 - 0.0035048*x5 + 0.047228*x6

    dydt = [x1_dot, x2_dot, x3_dot, x4_dot, x5_dot, x6_dot, y1]
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
        newt.append(float(format(step, '.2f')))
    t = newt

    u1 = initialCondition[7]

    sol = odeint(BM_dynamic, initialCondition[0:7], t, args=(u1,), hmax = time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,6]))
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
