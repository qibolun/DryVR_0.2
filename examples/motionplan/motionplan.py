from scipy.integrate import odeint
import numpy as np

def motion_dynamic(y, t, u1, u2):
    X1, X2, X3 = y
    X1_dot = u1
    X2_dot = u2
    X3_dot = X2 * u2
    dydt = [X1_dot, X2_dot, X3_dot]
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

    u1, u2 = map(float,Mode.split('_'))
    sol = odeint(motion_dynamic,initialCondition,t,args=(u1, u2),hmax = time_step)
    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        tmp.append(float(sol[j,2]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":
    sol = TC_Simulate('1_1',[1.0,0.0,1.0],10)
    for s in sol:
        print(s)
