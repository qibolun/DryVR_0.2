from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/lac-operon/ 

def lac_operon_dynamic(y,t):
    Ii, G = y
    Ii = float(Ii)
    G = float(G)

    Ii_dot = -0.4 * Ii**2 *( (0.0003*G**2 + 0.008) / (0.2*Ii**2 + 2.00001) ) + 0.012 + (0.0000003 * (54660 - 5000.006*Ii) * (0.2*Ii**2 + 2.00001)) / (0.00036*G**2 + 0.00960018 + 0.000000018*Ii**2)
    G_dot = -0.0006*G**2 + (0.000000006*G**2 + 0.00000016) / (0.2*Ii**2 + 2.00001) + (0.0015015*Ii*(0.2*Ii**2 + 2.00001)) / (0.00036*G**2 + 0.00960018 + 0.000000018*Ii**2)

    dydt = [Ii_dot, G_dot]
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

    sol = odeint(lac_operon_dynamic, initialCondition, t, hmax=time_step)

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

    sol = TC_Simulate("Default", [1, 25], 150.0)
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
