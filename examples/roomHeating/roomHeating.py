from scipy.integrate import odeint
import numpy as np

def roomTemp_dynamic(y, t, mode):
    T1, T2, T3 = y
    T1_dot = -0.105*T1+0.05*T2+0.05*T3+0.05
    T2_dot = 0.05*T1-0.105*T2+0.05*T3+0.05
    T3_dot = 0.05*T1+0.05*T2-0.105*T3+0.05
    if mode == "ON_1":
        T1_dot = -0.105*T1+0.05*T2+0.05*T3+0.05+0.5-0.01*T1
    if mode == "ON_2":
        T2_dot = 0.05*T1-0.105*T2+0.05*T3+0.05+0.5-0.01*T2
    if mode == "ON_3":
        T3_dot = 0.05*T1+0.05*T2-0.105*T3+0.05+0.5-0.01*T3
    dydt = [T1_dot, T2_dot, T3_dot]
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
    sol = odeint(roomTemp_dynamic,initialCondition,t,args=(Mode,),hmax = time_step)
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
    sol = TC_Simulate('ON_1',[22.0,22.0,22.0],10)
    for s in sol:
        print(s)
