from scipy.integrate import odeint
import numpy as np

def nav_dynamic(y, t, modeNum):
    px, py, vx, vy = y
    px_dot = vx
    py_dot = vy
    if modeNum == 1:
        vx_dot = -1.2*vx+0.1*vy-0.1
        vy_dot = 0.1*vx-1.2*vy+1.2
    elif modeNum == 2:
        vx_dot = -1.2*vx+0.1*vy-4.8
        vy_dot = 0.1*vx-1.2*vy+0.4
    elif modeNum == 3:
        vx_dot = -1.2*vx+0.1*vy+2.4
        vy_dot = 0.1*vx-1.2*vy-0.2
    else:
        vx_dot = -1.2*vx+0.1*vy+3.9
        vy_dot = 0.1*vx-1.2*vy-3.9
    return [px_dot, py_dot, vx_dot, vy_dot]

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
    while t[-1] == t[-2]:
        t.pop()

    modeNum = int(Mode[-1])

    sol = odeint(nav_dynamic,initialCondition,t,args=(modeNum,),hmax = time_step)
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

if __name__ == "__main__":
    ret = TC_simulate("Zone3", [0.5, 0.5, 0.0, 0.0], 2)
    for r in ret:
        print r
