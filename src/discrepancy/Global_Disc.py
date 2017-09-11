"""
This file contains core bloating algorithm for dryvr
It is very messy. I will rewrite this part eventually!
"""

from numpy import log, exp

import glpk
import numpy as np
import matplotlib.pyplot as plt
import time

# Global vars
dimensions = 0
dimensions_nt = 0
trace_len = 0
start_time = 0.0
end_time = 0.0
#init_delta = 'inf'
n = 100

"""
traces_path = '../Power_Train_Model1/traces.txt'
center_path = '../Power_Train_Model1/center_trace.txt'
"""
"""
traces_path = '../E_REV_CDCS/E_REV_CDCS/traces2.txt'
center_path = '../E_REV_CDCS/E_REV_CDCS/center_trace2.txt'
"""

traces_path = 'output/other_traces.txt'
center_path = 'output/center_trace.txt'

# Read in all the traces
def read_data(traces):

    global dimensions
    global dimensions_nt
    global trace_len
    global start_time
    global end_time

    # Locals
    trace = traces[0]
    error_thred_time = 1e-6

    # Calculate variables
    dimensions = len(trace[0])
    dimensions_nt = dimensions - 1
    #trace_len = len(trace)
    #start_time = trace[0][0]
    end_time = trace[-1][0]

    # Align all the traces
    for i in range (len(traces)):
    	initial_time = traces[i][0][0]
    	for j in range (len(traces[i])):
    		traces[i][j][0] = traces[i][j][0] - initial_time

    #reasign the start time and end time
    start_time = 0;
    for i in range (len(traces)):
    	end_time = min(end_time,traces[i][-1][0])

    #trim all the points after the end time
    traces_trim = [];
    for i in range (len(traces)):
    	trace_trim = [];
    	for j in range (len(traces[i])):
    		if traces[i][j][0] <= end_time + error_thred_time:
    			trace_trim.append(traces[i][j])
    	traces_trim.append(trace_trim)
    	#print(len(trace_trim))

    #reasign trace_len
    trace_len = len(trace_trim)

    
    return traces_trim


def A_calc(traces):
    global trace_len
    trace = traces[0]
    A = []
    for i in range(trace_len-1):
        A.append([-1, -(trace[i+1][0]-trace[0][0])])  # [-1, -(t(i+1)-t0)]

    # write A matrix to file
    # with open('./A.txt', 'w') as write_file:
    #     for i in range(len(A)):
    #         write_file.write(str(A[i])+ '\n')
    return A

def b_calc(traces,dim, init_delta):
    global trace_len
    global num_traces
    #global init_delta

    b = []

    #print(trace_len)
    #init_delta = abs(traces[0][0][dim] - traces[1][0][dim])

    # check traces number; if too few traces, give up
    num_traces = len(traces)
    if num_traces < 3:
        print("Only have " + str(num_traces-1) + " sample traces! Give up!")
        return None

    # compute b matrix
    for i in range(trace_len-1):   # t = t(i+1)
        maxval = -float('Inf')

        # select any of the two traces and compute their difference in value at t(i+1)
        for j in range(num_traces):
            for k in range(j+1,num_traces):
                trace1 = traces[j]
                trace2 = traces[k]
                #init_delta = max(init_delta,abs(trace1[0][dim]-trace2[0][dim]))
                #print(i)
                #rint(len(trace1))
                #print(len(trace2))
                if abs(trace1[0][dim]-trace2[0][dim]) <= 1e-6:
                    # print("Same trace detected! Algorithm stops!")
                    # print("These two traces are the same trace:")
                    # print("trace",j)
                    # print("trace",k)
                    return 'Same_trace!'
                if trace1[i+1][dim]-trace2[i+1][dim] == 0:
                    val = -float('Inf')
                else:
                    val = log(abs(trace1[i+1][dim]-trace2[i+1][dim]))-log(abs(trace1[0][dim]-trace2[0][dim]))
                if val > maxval:
                    maxval = val
        b.append(-maxval)

    # write b matrix to file
    # with open('./b.txt', 'w') as write_file:
    #     for i in range(len(b)):
    #         write_file.write(str(b[i])+ '\n')

    #init_delta = init_delta
    return b

def c_calc(traces):
    global start_time
    global end_time
    global n
    c = [n, (n+1)/2*(end_time-start_time)]  # (1/n + 2/n + ... + 1)*(T-t0)

    # write objective coefficients to file
    # with open('./c.txt', 'w') as write_file:
    #     write_file.write(str(c)+ '\n')
    return c

def k_gamma_calc(A, b, c):

    # use scipy.optimize.linprog
    """
    from scipy.optimize import linprog
    k_bounds = (0, None)    # k >= 1, i.e. log(k) >= 0
    gamma_bounds = (None, None)
    res = linprog(c, A_ub=A, b_ub=b, bounds=(k_bounds, gamma_bounds))
    k = exp(res.x[0])
    gamma = res.x[1]
    """

    # use glpk
    
    lp = glpk.LPX()
    lp.name = 'logk_gamma'
    lp.obj.maximize = False             # set this as a minimization problem
    lp.rows.add(len(A))                 # append rows to this instance
    for i in range(len(b)):
        lp.rows[i].bounds = None, b[i]  # set bound: entry <= b[i]
    lp.cols.add(2)                      # append two columns for k and gamma to this instance
    lp.cols[0].name = 'logk'
    lp.cols[0].bounds = 0.01, 10.0     # k >= 1, i.e. log(k) >= 0
    lp.cols[1].name = 'gamma'
    lp.cols[1].bounds = None, None      # no constraints for gamma
    lp.obj[:] = c                       # set objective coefficients
    lp.matrix = np.ravel(A)             # set constraint matrix; convert A to 1-d array
    lp.simplex()                        # solve this LP with the simplex method
    k = exp(lp.cols[0].primal)
    gamma = lp.cols[1].primal
    
    return k, gamma

#Main part
# start = time.time()

# dim = 1     # dimension index of the variable we want to calculate coefficients for




def Global_Discrepancy(Mode, init_delta_array, plot_flag, plot_dim,traces):
    global dimensions
    read_data(traces)

    # The returned value
    k_values = []
    gamma_values = []

    for dim in range(1,dimensions):
        init_delta = init_delta_array[dim-1]
        A = A_calc(traces)
        if b_calc(traces,dim,init_delta) == 'Same_trace!':
            #print('Same initial condition detected for dimension %d, using default value' % (dim))
            k = 1
            gamma = 0
        else:
            b = b_calc(traces,dim,init_delta)
            c = c_calc(traces)
            #print("finish coefficients")
            if b == None:
                print("Error!")
            else:
                k, gamma = k_gamma_calc(A,b,c)
                # print("k =",k)
                # print("gamma =",gamma)
        k_values.append(k)
        gamma_values.append(gamma)

# end = time.time()
# print("Time spent on computing coefficient = "+str(end-start)+"s")
# print(init_delta)

# plot results
    if plot_flag:
        k = k_values[plot_dim-1]
        gamma = gamma_values[plot_dim-1]
        init_delta = init_delta_array[plot_dim-1]
        center_trace = traces[0]
        minval = float('Inf')
        maxval = -float('Inf')
        # compute reach tube upper/lower bound point-by-point
        upper_bound_trace = [center_trace[0][plot_dim]+init_delta]
        lower_bound_trace = [center_trace[0][plot_dim]-init_delta]
        for i in range(trace_len-1):
            time_interval = center_trace[i+1][0] - center_trace[0][0] # time_interval = t(i+1) - t0
            delta = k * exp(gamma*time_interval) * init_delta
            upper_bound_trace.append(center_trace[i+1][plot_dim]+delta)
            lower_bound_trace.append(center_trace[i+1][plot_dim]-delta)

        #print(upper_bound_trace[-1]-lower_bound_trace[-1])
        center_trace = traces[0]
        time = [row[0] for row in center_trace]
        plt.plot(time,[row[plot_dim] for row in center_trace],'-r',label="center trace") # center trace in color red
        for i in range(1,num_traces):
            trace = traces[i]
            plt.plot(time,[row[plot_dim] for row in trace],'-b') # other traces in color blue
        plt.plot(time,upper_bound_trace,'-y',label="reach tube bound") # upper bound trace in color yellow
        plt.plot(time,lower_bound_trace,'-y') # lower bound trace in color yellow
        plt.title("k = "+str(k)+"; gamma = "+str(gamma))
        plt.legend()
        plt.show()
        plt.savefig('books_read.png')
    return k_values, gamma_values

def Bloat_to_tube(Mode, k, gamma, init_delta_array, write_path, write_type, concatTime, traces):
    global dimensions
    read_data(traces)
    center_trace = traces[0]
    reach_tube = []
    timeLow = concatTime[0]
    timeUp = concatTime[1]

    # Compute the reach_tube
    for i in range(trace_len-1):
        time_interval = center_trace[i+1][0] - center_trace[0][0] # time_interval = t(i+1) - t0
        lower_rec = [center_trace[i][0]]
        upper_rec = [center_trace[i+1][0]]
        for dim in range(1,dimensions):
            delta = k[dim-1] * exp(gamma[dim-1]*time_interval) * init_delta_array[dim-1]
            upper_rec.append(max(center_trace[i+1][dim],center_trace[i][dim])+delta)
            lower_rec.append(min(center_trace[i+1][dim],center_trace[i][dim])-delta)
        lower_rec.append(lower_rec[0]+timeLow)
        upper_rec.append(upper_rec[0]+timeUp)
        reach_tube.append(lower_rec)
        reach_tube.append(upper_rec)

    if write_type == 'new':       
        with open(write_path, 'w') as write_file:
            write_file.write(Mode + '\n')
            for i in range(len(reach_tube)):
                for j in range(len(reach_tube[0])):
                    write_file.write(str(reach_tube[i][j]) + ' ')
                write_file.write('\n')
    elif write_type == 'append':
        with open(write_path, 'a') as write_file:
            #write_file.write(Mode + '\n')
            for i in range(len(reach_tube)):
                for j in range(len(reach_tube[0])):
                    write_file.write(str(reach_tube[i][j]) + ' ')
                write_file.write('\n')
    else:
        print('writing type wrong!')
    return reach_tube


def writeTraceToFile(Mode, reach_tube, write_path, write_type):
    if write_type == 'new':
        with open(write_path, 'w') as write_file:
            write_file.write(Mode + '\n')
            for i in range(len(reach_tube)):
                for j in range(len(reach_tube[0])):
                    write_file.write(str(reach_tube[i][j]) + ' ')
                write_file.write('\n')
    elif write_type == 'append':
        with open(write_path, 'a') as write_file:
            for i in range(len(reach_tube)):
                for j in range(len(reach_tube[0])):
                    write_file.write(str(reach_tube[i][j]) + ' ')
                write_file.write('\n')
    else:
        print('writing type wrong!')
    return reach_tube



def Bloat_to_tubeNoIO(Mode, k, gamma, init_delta_array, concatTime, traces):
    global dimensions
    read_data(traces)
    center_trace = traces[0]
    reach_tube = []
    timeLow = concatTime[0]
    timeUp = concatTime[1]

    for i in range(trace_len-1):
        time_interval = center_trace[i+1][0] - center_trace[0][0]
        lower_rec = [center_trace[i][0]]
        upper_rec = [center_trace[i+1][0]]

        for dim in range(1,dimensions):
            delta = k[dim-1] * exp(gamma[dim-1]*time_interval) * init_delta_array[dim-1]
            upper_rec.append(max(center_trace[i+1][dim],center_trace[i][dim])+delta)
            lower_rec.append(min(center_trace[i+1][dim],center_trace[i][dim])-delta)
        lower_rec.append(lower_rec[0]+timeLow)
        upper_rec.append(upper_rec[0]+timeUp)
        reach_tube.append(lower_rec)
        reach_tube.append(upper_rec)
    return reach_tube

def bloatToTube(mode, k, gamma, init_delta_array, traces):
    global dimensions
    read_data(traces)
    center_trace = traces[0]
    reach_tube = []

    for i in range(trace_len-1):
        time_interval = center_trace[i+1][0] - center_trace[0][0]
        lower_rec = [center_trace[i][0]]
        upper_rec = [center_trace[i+1][0]]

        for dim in range(1,dimensions):
            delta = k[dim-1] * exp(gamma[dim-1]*time_interval) * init_delta_array[dim-1]
            upper_rec.append(max(center_trace[i+1][dim],center_trace[i][dim])+delta)
            lower_rec.append(min(center_trace[i+1][dim],center_trace[i][dim])-delta)
        reach_tube.append(lower_rec)
        reach_tube.append(upper_rec)
    return reach_tube

