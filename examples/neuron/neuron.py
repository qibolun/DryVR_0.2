from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math

def TWModel_dynamics(V,t,W_gap,W_syn,knockOut):
    # Some constants
    V_leak = -0.035
    g_gap = 5e-9
    g_syn = 6e-10
    V_Range = 0.035
    K=-4.3944
    Cap = np.array([5,9.1,9.1,14,15,16,14,16,15])*1e-12
    Res = np.array([30,16,16,11,10,9.4,11,9.4,10])*1e9
    E_syn = np.array([-0.048,-0.048,-0.048,0,-0.048,0,-0.048,-0.048,-0.048])
    N = 9

    # if knockOut == 0:
    #     W_gap = W_gap
    #     W_syn = W_syn
    # else:

    # Simulation of TW circuit 
    simdur = 0.06  # (60 mS)
    dt = 0.00005    
    pulse_stim = 5e-10  # Stimulation strength
    startTime = 0.01  # time when stimulation is started  
    pulse_dur = 0.03  # stimulation duration

    simStep = simdur/dt
    IStim = np.zeros([N,simStep+1], dtype = int)
    startInd = int(startTime/dt)
    endInd = int((startTime+pulse_dur)/dt)
    for i in range(1,3):
        for j in range(startInd, endInd):
            IStim[i][j] = pulse_stim

    # Calculate V_eq
    A = np.zeros([N,N])
    B = np.zeros(N)
    for i in range(0, N):
        for j in range(0,N):
            if i != j:
                A[i][j] = -Res[i] * W_gap[i][j] * g_gap
            else:
                for k in range(0,N):
                    A[i][j] = 1 + Res[i] * (W_gap[i][k] * g_gap * g_syn * 1/2)
        
        for l in range(0,N):
            B[i] = V_leak + Res[i] * (E_syn[l] * W_syn[i][l] * g_syn * 1/2)
    
    V_eq = np.linalg.solve(A,B)
    # print V_eq
    # initialize the arguments
    I_stim = np.zeros(N)
    I_leak = np.zeros(N)
    I_gap = np.zeros(N)
    I_syn = np.zeros(N)
    g = np.empty([N,N],dtype=int)
    V_dot = np.zeros(N)

    # Components of differential equation
    for i in range(0, N):
        I_stim[i] = IStim[i][round(t/dt)+1]
        I_leak[i] = (V_leak - V[i])/Res[i]
        for j in range(0,N):
            I_gap[i] += g_gap*W_gap[i][j]*(V[j]-V[i])
            g[i][j] = g_syn/(1+np.exp(K*(V[j]-V_eq[j])/V_Range))
            I_syn[i] += W_syn[i][j]*g[i][j]*(E_syn[j]-V[i])

        V_dot[i] = (I_leak[i]+I_gap[i]+I_syn[i]+I_stim[i])/Cap[i]

    dydt = [V_dot[0], V_dot[1], V_dot[2], V_dot[3], V_dot[4], V_dot[5], V_dot[6], V_dot[7], V_dot[8]]
    return dydt


def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.005;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    # Some constants 
    knockOut = 0
    W_gap = [[0, 2, 0, 1, 0, 0, 0, 0, 0], [2, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 10, 0, 0, 0], [0, 0, 2, 0, 10, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 2, 0, 0]]

    W_syn = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 5, 0, 2, 8, 3, 0, 0], [0, 0, 5, 70, 0, 14, 27, 27, 3], [10, 9, 1, 1, 28, 0, 0, 28, 4], 
            [12, 0, 0, 1, 2, 27, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 5, 0, 0, 4, 0, 3, 0]]

    sol = odeint(TWModel_dynamics, initialCondition, t, args=(W_gap, W_syn, knockOut), hmax=time_step)

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

    sol = TC_Simulate("Default", [-0.0281,-0.0281,-0.0337,-0.0280,-0.0273,-0.0337,-0.0161,-0.0092,-0.0240], 0.06)
    #for s in sol:
	#	print(s)

    time = [row[0] for row in sol]

    a = [row[1] for row in sol]

    b = [row[2] for row in sol]

    # plt.plot(time, a, "-r")
    # plt.plot(time, b, "-g")
    # plt.show()
    # plt.plot(a, b, "-r")
    # plt.show()
