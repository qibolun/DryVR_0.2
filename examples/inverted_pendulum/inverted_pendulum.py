from scipy.integrate import odeint
import numpy as np
from math import cos, sin
def pendulum_dynamic(y, t, u):
    theta, omega = y
    theta_dot = omega
    omega_dot = 4.9*sin(theta)-4*omega+2*cos(theta)*u

    dydt = [theta_dot, omega_dot]
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
    sol = odeint(pendulum_dynamic,initialCondition,t,args=(float(Mode),),hmax = time_step)
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
    sol = TC_Simulate('-1',[0.2,0.3],10)
    for s in sol:
        print(s)
