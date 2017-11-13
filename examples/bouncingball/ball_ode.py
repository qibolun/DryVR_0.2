from scipy.integrate import odeint
import numpy as np

def Ball_dynamic(y, t):
    hy, v = y
    hy_dot = v
    v_dot = -9.8
    dydt = [hy_dot, v_dot]
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
    sol = odeint(Ball_dynamic,initialCondition,t,hmax = time_step)
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
    sol = TC_Simulate('BOUNCE',[100.0,0.0],10)
    for s in sol:
        print(s)
