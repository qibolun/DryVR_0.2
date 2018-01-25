from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Source: https://ths.rwth-aachen.de/research/projects/hypro/van-der-pol-oscillator/

def vanderpol_dynamic(y,t, mode):
    e1,e1prime,a1,e2,e2prime,a2,e3,e3prime,a3 = y
    if mode == "l1":
        e1_dot = e1prime
        e1prime_dot = -a1
        a1_dot = 1.605*e1 + 4.868*e1prime - 3.5754*a1 - 0.8198*e2 + 0.427*e2prime - 0.045*a2 - 0.1942*e3 + 0.3626*e3prime - 0.0946*a3
        e2_dot = e2prime
        e2prime_dot = a1 - a2
        a2_dot = 0.8718*e1 + 3.814*e1prime - 0.0754*a1 + 1.1936*e2 + 3.6258*e2prime - 3.2396*a2 - 0.595*e3 + 0.1294*e3prime - 0.0796*a3
        e3_dot = e3prime
        e3prime_dot = a2 - a3
        a3_dot = 0.7132*e1 + 3.573*e1prime - 0.0964*a1 + 0.8472*e2 + 3.2568*e2prime - 0.0876*a2 + 1.2726*e3 + 3.072*e3prime - 3.1356*a3
    elif mode == "l2":
        e1_dot = e1prime
        e1prime_dot = -a1
        a1_dot = 1.605*e1 + 4.868*e1prime - 3.5754*a1
        e2_dot = e2prime
        e2prime_dot = a1 - a2
        a2_dot = 1.1936*e2 + 3.6258*e2prime - 3.2396*a2
        e3_dot = e3prime
        e3prime_dot = a2 - a3
        a3_dot = 0.7132*e1 + 3.573*e1prime - 0.0964*a1 + 0.8472*e2 + 3.2568*e2prime - 0.0876*a2 + 1.2726*e3 + 3.072*e3prime - 3.1356*a3



    dydt = [e1_dot, e1prime_dot, a1_dot, e2_dot, e2prime_dot, a2_dot, e3_dot, e3prime_dot, a3_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.02;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(vanderpol_dynamic, initialCondition, t, args=(Mode,), hmax=time_step)

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
        tmp.append(float(sol[j,8]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("l1", [1.0, 1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0], 2.0)
    for s in sol:
		print(s)

  