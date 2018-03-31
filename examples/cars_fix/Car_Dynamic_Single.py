# The differential equations of a single car dynamics

from scipy.integrate import odeint
from scipy.interpolate import interp1d
import numpy as np 

def Car_dynamic(y,t,v_initial,acc,turn_indicator,turn_time,turn_back_time):
    L = 5.0 # the length of the car, make it fix here
    # make everything double
    v_initial = float(v_initial)
    acc = float(acc)
    y = [float(tmp) for tmp in y]
    turn_time = float(turn_time)
    turn_back_time = float(turn_back_time)
    # end of making float

    # set the velocity

    # Speed upper bound = 108km/hr = 30m/s
    # speed lower bound = 0km/hr = 0m/s
    v = v_initial + acc*t
    if v>=30.0:
        v = 30.0
    if v<=0.0:
        v = 0.0
    # set the steering angle
    delta_initial = 0.0

    # The turn factor need to be based on the speed of the vehicle 
    # So that the we can always achieve a constant lane switch
    # turn_factor = 0.014 # this is the value when speed is 16.67
    # turn_factor = 0.22 # this is the value when speed is 4.17
    # turn_factor = 0.0043 # this is the value when speed is 30.0
    # turn_factor = 0.0097 # this is the value when speed is 20.0
    # turn_factor = 0.0061 # this is the value when speed is 25.0
    # turn_factor = 0.039 # this is the value when speed is 10.0
    # turn_factor = 0.060 # this is the value when speed is 8.0
    # turn_factor = 0.155 # this is the value when speed is 5.0
    # turn_factor = 0.43 # this is the value when speed is 3.0
    # turn_factor = 0.0052 # this is the value when speed is 27.5
    # turn_factor = 0.0125 # this is the value when speed is 17.5
    turn_factor = 0.025 # this is the value when speed is 1
    if turn_indicator == 'Left':
        # print(t)
        if t <= turn_time:
            delta_steer = delta_initial;
        elif (t > turn_time) and (t <= turn_time + 2.0):
            delta_steer = delta_initial + turn_factor
        elif (t > turn_time + 2.0) and (t <= turn_back_time):
            delta_steer = delta_initial 
        elif (t > turn_back_time) and (t <= turn_back_time + 2.0):
            delta_steer = delta_initial - turn_factor
        elif t > turn_back_time + 2.0:
            delta_steer = delta_initial
        else:
            print('Something is wrong with time here when calculting steering angle!')
    elif turn_indicator =='Right':
        if t <= turn_time:
            delta_steer = delta_initial;
        elif (t > turn_time) and (t <= turn_time + 2.0):
            delta_steer = delta_initial + (-turn_factor) 
        elif (t > turn_time + 2.0) and (t <= turn_back_time):
            delta_steer = delta_initial 
        elif (t > turn_back_time) and (t < turn_back_time + 2.0):
            delta_steer = delta_initial + (turn_factor)
        elif t > turn_back_time + 2.0:
            delta_steer = delta_initial
        else:
            print('Something is wrong with time here when calculting steering angle!')
    elif turn_indicator == 'Straight':
        delta_steer = delta_initial
    else:
        print('Wrong turn indicator!')

    psi, sx, py = y
    psi_dot = (v)/L*(np.pi/8.0)*delta_steer
    w_z = psi_dot
    sx_dot = v * np.cos(psi) - L/2.0 * w_z * np.sin(psi) 
    if abs(sx_dot) < 0.0000001:
        sx_dot = 0.0
    sy_dot = v * np.sin(psi) + L/2.0 * w_z * np.cos(psi)
    if abs(sy_dot) < 0.0000001:
        sy_dot = 0.0
    #sx_dot = v * np.cos(psi) 
    #sy_dot = v * np.sin(psi)
    dydt = [psi_dot, sx_dot, sy_dot]
    return dydt


def Car_simulate(Mode,initial,time_bound):
    time_step = 0.05;
    time_bound = float(time_bound)
    initial = [float(tmp)  for tmp in initial]
    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt
    # initial = [sx,sy,vx,vy]
    # set the parameters according to different modes
    # v_initial,acc,acc_time,turn_indicator,turn_time,turn_back_time

    sx_initial = initial[0]
    sy_initial = initial[1]
    vx_initial = initial[2]
    vy_initial = initial[3]

    v_initial = (vx_initial**2 + vy_initial**2)**0.5

    # calculate the initial angle
    val = np.arccos(vx_initial/v_initial)
    if vy_initial < 0:
        val = 2*np.pi-val
    psi_initial = val
    acc = 0.0
    turn_time = 0.0
    turn_back_time = 0.0

    # Initialize according to different mode
    if Mode == 'Const':
        turn_indicator = 'Straight'
    elif ((Mode == 'Acc1') or (Mode == 'Acc2')):
        turn_indicator = 'Straight'
        acc = 1.0
    elif (Mode == 'Dec'): 
        turn_indicator = 'Straight'
        acc = -1.0
    elif (Mode == 'Brk'):
        turn_indicator = 'Straight'
        acc = -5.0

    elif Mode =='TurnLeft':
        turn_indicator = 'Left'
        turn_time = 0.0
        turn_back_time = 5.0

    elif Mode == 'TurnRight':
        turn_indicator = 'Right'
        turn_time = 0.0
        turn_back_time = 5.0

    else:
        print('Wrong Mode name!')

    Initial_ode = [psi_initial, sx_initial, sy_initial]
    sol = odeint(Car_dynamic,Initial_ode,t,args=(v_initial,acc,turn_indicator,turn_time,turn_back_time),hmax = time_step)

    # Construct v
    v = np.zeros(len(t))
    # Speed upper bound = 108km/hr = 30m/s
    # speed lower bound = 0km/hr = 0m/s
    for i in range(len(t)):
        fv = v_initial + acc*t[i]
        if fv>=30.0:
            fv = 30.0
        if fv<=0.0:
            fv = 0.0
        v[i] = fv

    # Construct the final output
    trace = []
    for j in range(len(t)):
        current_psi = sol[j,0]
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(sol[j,1])
        tmp.append(sol[j,2])
        

        vx = v[j]*np.cos(current_psi)
        if abs(vx) < 0.0000001:
            vx = 0.0
        tmp.append(vx)
        vy = v[j]*np.sin(current_psi)
        if abs(vy) < 0.0000001:
            vy = 0.0
        tmp.append(vy)
        trace.append(tmp)
    return trace

if __name__ == "__main__":
    print "start test"
    # 16.67*3.6 = 60km/hr
    traj = Car_simulate("TurnLeft", [0.0,0.0,0.0,12.5], "10")
    for line in traj:
        print line
    # x = [16.67, 4.17, 30.0, 20.0, 25.0, 10.0,8.0,5.0,3.0,27.5,17.5,2,1]
    # y = [0.014,0.22,0.0043,0.0097,0.0061,0.039,0.069,0.155,0.43,0.0052,0.0125,0.97,]
    speed = 30
    print 0.143486*np.exp(-0.134119*speed)
    print np.exp(-45.17)
    


