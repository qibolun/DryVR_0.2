from scipy.integrate import odeint
import numpy as np

def Ball_dynamic(y, t):
    px, py, vx, vy = y
    px_dot = vx
    py_dot = vy
    vx_dot = 0
    vy_dot = 0
    dydt = [px_dot, py_dot, vx_dot, vy_dot]
    return dydt


def Ball_simulate(Mode,initialCondition,time_bound):
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
    while t[-1] == t[-2]:
        t.pop()

    sol = odeint(Ball_dynamic,initialCondition,t,hmax = time_step)
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
