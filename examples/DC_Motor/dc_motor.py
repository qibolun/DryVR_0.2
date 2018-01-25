from scipy.integrate import odeint
import numpy as np

def circuit_dynamic(y, t, u):
    X1, X2 = y
    R = 500 * 10**-3
    L = 1500 * 10**-6
    J = 250 * 10**-6
    B = 100 * 10**-6
    k = 50 * 10**-3

    X1_dot = -(B*X1)/J + (k*X2)/J
    X2_dot = -(k*X1)/L - (R*X2)/L + u/L

    dydt = [X1_dot, X2_dot]
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
    while t[-1] == t[-2]:
        t.pop()

    sol = odeint(circuit_dynamic,initialCondition,t,args=(float(Mode),),hmax = time_step)
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
    sol = TC_Simulate('10',[10.0, 5.0],10)
    for s in sol:
        print(s)
