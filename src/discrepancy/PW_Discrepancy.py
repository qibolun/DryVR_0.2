from __future__ import division
import matplotlib.pyplot as plt
import math, pdb, traceback, sys
#import hashlib

# Constants
# P_DIM = 4
# Initial_Delta = [0.01,0.1,0.01,0.005]

# Global vars
# dimensions = 0
# dimensions_nt = 0;
# trace_len = 0
# delta_time = 0.0
# end_time = 0.0
# K_value = 38
#K_value = 21.5
# K_value = [1.0,1.0,2.0,1.0,1.0,2.0]
# num_ti = []


# Global lists
# traces = []
# traces_diff = []
# time_intervals = []
# discrepancies = []
# bloat_tube = []

traces_path = 'output/other_traces.txt'
center_path = 'output/center_trace.txt'

# Read in all the traces
def read_data(traces):

    error_thred_time = 1e-3

    trace = traces[0]
    delta_time = trace[1][0] - trace[0][0]

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
    traces_trim = traces
    # for i in range (len(traces)):
    #     trace_trim = [];
    #     for j in range (len(traces[i])):
    #         if traces[i][j][0] <= end_time + error_thred_time:
    #             trace_trim.append(traces[i][j])
    #     traces_trim.append(trace_trim)
        #print(len(trace_trim))

    #reasign trace_len
    trace_len = len(traces_trim[0])
    #print(traces_trim)
    return (traces_trim,dimensions,dimensions_nt,trace_len,end_time,delta_time,start_time)

# Compute difference between traces
def compute_diff(traces):
    # Iterate over all combinations
    #global P_DIM
    traces_diff = []
    for i in xrange(0, len(traces)):
        for j in xrange(i + 1, len(traces)):

            trace_diff = []

            # Iterate over the data of the trace
            for t in xrange(0, len(traces[i])):
                diff = [abs(x_i - y_i) for x_i, y_i in zip(traces[i][t],
                    traces[j][t])]
                trace_diff.append(diff[1:])

            # Append to traces diff minus time difference
            traces_diff.append(trace_diff)
    #print(traces_diff)

    with open('output/tracediff2.txt', 'w') as write_file:
        for i in range(len(traces_diff)):
            for j in range(len(traces_diff[0])):
 #               print(i,j)
                write_file.write(str(traces_diff[i][j]) + '\n')
            write_file.write('\n')
    return traces_diff

# Compute the time intervals
def find_time_intervals(traces_diff,dimensions_nt,end_time,trace_len,delta_time,K_value):
    # FIXME just do 1 dimension for now
    # Iterate through all dimensions
    num_ti = []
    time_intervals = []

    for i in xrange(0, dimensions_nt):
    #for i in xrange(0, P_DIM):

        time_dim = []


        # Obtain difference at start of interval
        diff_0 = []
        t_0 = 0.0
        time_dim.append(t_0);
        for k in xrange(0, len(traces_diff)):
            diff_0.append(traces_diff[k][0][i])
        # Iterate through all points in trace

        #pdb.set_trace()
        #for j in xrange(0, trace_len):
        for j in xrange(1, trace_len):
            # Obtain difference at ith time of interval
            diff_i = []
            try:
                for k in xrange(0, len(traces_diff)):
                    diff_i.append(traces_diff[k][j][i])
            except:
                print trace_len
                print k,j,i
                print len(traces_diff[k])
                print len(traces_diff[k][j])


            # Check time
            t_i = j * delta_time;
            t = t_i - t_0
            if t <= 0:
                continue

            # Compute ratios
            ratio = []
            for d_0, d_i in zip(diff_0, diff_i):
                if d_i < 1E-3:
                    continue
                elif d_0 < 1E-3:
                    continue

                # NOTE not sure if this is right?
                #ratio.append((1 / t) * math.log(d_i / d_0))
                ratio.append(d_i / d_0)

            # Check ratios if less than constant
            # new_int = all(r <= 2.0*K_value[i] for r in ratio)
            # new_int = all(r <= 2**(2*t)*K_value[i] for r in ratio)
            new_int = all(r <= 1 for r in ratio)
            if new_int == False:
            	if t_i != end_time:
            		time_dim.append(t_i)
                diff_0 = diff_i
                t_0 = t_i

        # Append the time intervals
        time_dim.append(end_time)
        time_intervals.append(time_dim)
        #record the number of time intervals
        num_ti.append(len(time_intervals[i]) - 1)

    # Print time_intervals
    # print('Time intervals: ')
    # print(time_intervals)
    # print('')

    return (time_intervals, num_ti)


# Compute discrepancies
def calculate_discrepancies(time_intervals,traces_diff,dimensions_nt,delta_time,K_value):
    # FIXME
    # Iterate over all dimensions
    discrepancies = []
    for nd in xrange(0, dimensions_nt):
    #for nd in xrange(0, P_DIM):
        disc = []



        # Iterate over all time intervals
        for ni in xrange(0, len(time_intervals[nd]) - 1):
            t_0 = time_intervals[nd][ni]
            t_e = time_intervals[nd][ni + 1]
            #t_i = t_0 + delta_time

            # FIXME (???)
            # print "note",delta_time
            points = int((t_e - t_0) / delta_time + 0.5) + 1
            idx = int(t_0 / delta_time)

            # try to find the best K and gamma
            tmp_K_value = K_value[nd]
            # Iterate over all trace difference
            glpk_rows = []
            close_flag = 0
            for k in xrange(0, len(traces_diff)):

                # Compute initial
                diff_0 = traces_diff[k][0][nd]
                if diff_0 <= 1E-3:
                    #print('Find two traces to be too closed!')
                    #print('use the default value!')
                    close_flag = 1
                    break
                ln_0 = math.log(diff_0)

                # FIXME need to reset the delta_time here
                t_i = t_0 + delta_time
                #print(disc)
                # Obtain rows for GLPK
                for r in xrange(1, points):
                    t_d = t_i - t_0
                    t_i += delta_time
                    diff_i = traces_diff[k][idx + r][nd]

                    if diff_i < 1E-3:
                        continue

                    ln_i = math.log(diff_i)

                    #compute the existing previous time interval discrepancy
                    discrepancy_now = 0
                    if len(disc) != 0:
                    	for time_prev in range(0,len(disc)):
                    		discrepancy_now = discrepancy_now + disc[time_prev]*(time_intervals[nd][time_prev+1]-time_intervals[nd][time_prev])

                    ln_d = ln_i - ln_0 - math.log(tmp_K_value)- discrepancy_now
                    glpk_rows.append([t_d, ln_d])

            # Debugging algebraic solution
            if close_flag ==0:
                alg = [d / t for t, d in glpk_rows]
                if len(alg) != 0:
                    alg_max = max(alg)
                else:
                    alg_max = 0
            else:
                alg_max = 0

            disc.append(alg_max)

            #print('test print')
            #print disc


        # Append discrepancies
        discrepancies.append(disc)

    # Print discrepancies
    # print('Discrepancies:')
    # print(discrepancies)
    return discrepancies

# Obtain bloated tube
def generate_bloat_tube(traces, time_intervals,discrepancies,Initial_Delta,end_time,trace_len,dimensions_nt,delta_time,K_value):


    # timeLow = concatTime[0]
    # timeUp = concatTime[1]
    #global end_time

    # Iterate over all dimensions
    # FIXME
    #pdb.set_trace()
    bloat_tube = []
    for i in range(trace_len):
        bloat_tube.append([])
        bloat_tube.append([])

    for nd in xrange(0, dimensions_nt):
    #for nd in xrange(P_DIM - 1, P_DIM):

        time_bloat = []
        low_bloat = []
        up_bloat = []

        # To construct the reach tube
        time_tube = []
        tube = []

        prev_delta = Initial_Delta[nd]

        # Iterate over all intervals
        previous_idx = -1

        for ni in xrange(0, len(time_intervals[nd]) - 1):
            t_0 = time_intervals[nd][ni]
            t_e = time_intervals[nd][ni + 1]

            if t_e == end_time:
                points = int((t_e - t_0) / delta_time + 0.5)+1
            else:
                points = int((t_e - t_0) / delta_time + 0.5)
            idx = int(t_0 / delta_time)

            gamma = discrepancies[nd][ni]


            # Iterate over all points in center trace
            for r in xrange(0, points):

                current_idx = idx + r

                if current_idx != previous_idx + 1:
                    # print('Index mismatch found!')
                    if current_idx == previous_idx:
                        idx += 1
                    elif current_idx == previous_idx+2:
                        idx -= 1

                pnt = traces[0][idx + r]
                pnt_time = pnt[0]
                pnt_data = pnt[nd+1]

                cur_delta = prev_delta * math.exp(gamma * delta_time)
                max_delta = max(prev_delta, cur_delta)

                time_bloat.append(pnt_time)
                low_bloat.append(pnt_data - max_delta*K_value[nd])
                up_bloat.append(pnt_data + max_delta*K_value[nd])
                #low_bloat.append(pnt_data - max_delta*1.0)
                #up_bloat.append(pnt_data + max_delta*1.0)


                if nd == 0:
                    bloat_tube[2*(idx+r)].append(pnt_time)
                    bloat_tube[2*(idx+r)].append(pnt_data - max_delta*K_value[nd])
                    bloat_tube[2*(idx+r)+1].append(pnt_time+delta_time)
                    bloat_tube[2*(idx+r)+1].append(pnt_data + max_delta*K_value[nd])
                else:
                    bloat_tube[2*(idx+r)].append(pnt_data - max_delta*K_value[nd])
                    bloat_tube[2*(idx+r)+1].append(pnt_data + max_delta*K_value[nd])

                prev_delta = cur_delta

                previous_idx = idx + r

        # Debugging
        #range = -1
        #time_bloat = time_bloat[0:range]
        #low_bloat = low_bloat[0:range]
        #up_bloat = up_bloat[0:range]


        # Plot data
        # plt.plot(time_bloat, low_bloat, 'g')
        # plt.plot(time_bloat, up_bloat, 'g')
    #print(bloat_tube[58])
    # for i in range(0,len(bloat_tube),2):
    #     bloat_tube[i].append(bloat_tube[i][0]+timeLow)
    #     bloat_tube[i+1].append(bloat_tube[i+1][0]+timeUp)

    # if write_type == 'new':
    #     with open(write_path, 'w') as write_file:
    #         write_file.write(Mode + '\n')
    #         for i in range(len(bloat_tube)):
    #             for j in range(len(bloat_tube[0])):
    #  #               print(i,j)
    #                 write_file.write(str(bloat_tube[i][j]) + ' ')
    #             write_file.write('\n')
    # elif write_type == 'append':
    #     with open(write_path, 'a') as write_file:
    #         #write_file.write(Mode + '\n')
    #         for i in range(len(bloat_tube)):
    #             for j in range(len(bloat_tube[0])):
    #                 write_file.write(str(bloat_tube[i][j]) + ' ')
    #             write_file.write('\n')
    # else:
    #     print('writing type wrong!')
    return bloat_tube


# Write data to file
def write_to_file(time_intervals,discrepancies,write_path, type):
    # Write bloat file
    # if type == 'bloat':
    #     with open(write_path, 'w') as write_file:
    #         idx = 0
    #         for interval in bloat_tube:
    #             for b_ln in interval:
    #                 try:
    #                     c_pnt = traces[0][idx][P_DIM]
    #                 except:
    #                     type, value, tb = sys.exc_info()
    #                     traceback.print_exc()
    #                     pdb.post_mortem(tb)

    #                 idx += 1
    #                 write_file.write(str(b_ln[1]) + ' ' + str(c_pnt) + ' ' +
    #                         str(b_ln[2]) + '\n')

    # Write discrepancy file
    with open(write_path, 'w') as write_file:
        for i, disc_dim in enumerate(discrepancies):
            write_file.write('Dim ' + str(i) + ' discrepancies:\n')
            write_file.write('The K Value is ' + str(K_value[i]) + ' \n')
            for j in range(len(disc_dim)):
                write_file.write('['+ str(time_intervals[i][j]) + ' , ' + str(time_intervals[i][j+1]) + ']: ' + str(disc_dim[j]) + '\n')
            write_file.write('\n')

# Plat the traces
def plot_traces(traces,dim,bloat_tube):
    # Iterate over all individual traces
    for i in xrange(0, len(traces)):
        trace = traces[i]

        # Obtain desired dimension
        time = []
        data = []
        for j in xrange(0, len(trace)):
        #for j in xrange(0,2):
            time.append(trace[j][0])
            data.append(trace[j][dim])

        # Plot data
        if i == 0:
            plt.plot(time, data, 'b')
        else:
            plt.plot(time, data, 'r')

    time = [row[0] for row in bloat_tube]
    value = [row[dim] for row in bloat_tube]
    time_bloat = [time[i] for i in range(0,len(value),2)]
    lower_bound = [value[i] for i in range(0,len(value),2)]
    upper_bound = [value[i+1] for i in range(0,len(value),2)]
    plt.plot(time_bloat, lower_bound, 'g')
    plt.plot(time_bloat, upper_bound, 'g')

# Print out the intervals and discrepancies
def print_int_disc(discrepancies,time_intervals):
    for nd in xrange(0, len(discrepancies)):
        for p in xrange(0, len(discrepancies[nd])):
            print('idx: ' + str(p) + ' int: ' +str(time_intervals[nd][p])
                + ' to ' + str(time_intervals[nd][p+1]) + ', disc: ' +
                str(discrepancies[nd][p]))
        print('')

def PW_Bloat_to_tube(Initial_Delta,plot_flag,plot_dim,traces, K_value):
    # Read data in
    # if Mode == 'Const':
    #     K_value = [1.0,1.0,2.0]
    # elif Mode == 'Brake':
    #     K_value = [1.0,1.0,7.0]

    # if Mode == 'Const;Const':
    #     K_value = [1.0,1.0,2.0,1.0,1.0,2.0]
    # elif Mode == 'Brake;Const':
    #     K_value = [1.0,1.0,2.0,1.0,1.0,2.0]

    # elif Mode == 'Brake;Brake':
    #     K_value = [1.0,1.0,5.0,1.0,1.0,2.0]

    traces,dimensions,dimensions_nt,trace_len,end_time,delta_time,start_time = read_data(traces)
    # Compute difference between traces
    traces_diff =  compute_diff(traces)
    #print traces_diff

    # Find time intervals for discrepancy calculations
    time_intervals, num_ti = find_time_intervals(traces_diff,dimensions_nt,end_time,trace_len,delta_time,K_value)
    # print('number of time intervals:')
    # print num_ti
    # Discrepancy calculation
    discrepancies = calculate_discrepancies(time_intervals,traces_diff,dimensions_nt,delta_time,K_value)
    # print('The K values')
    # print K_value,
    #system.exit('test')

    # Write discrepancies to file
    #write_to_file(time_intervals,discrepancies,write_path +' disp.txt', 'disc')

    # Nicely print the intervals and discrepancies
    #print_int_disc(discrepancies,time_intervals)




    # Bloat the tube using time intervals
    reach_tube = generate_bloat_tube(traces,time_intervals,discrepancies,Initial_Delta,end_time,trace_len,dimensions_nt,delta_time,K_value)

    if plot_flag:
        plot_traces(traces,plot_dim,reach_tube)
        plt.show()

    return reach_tube






# def For_Test(Mode, Initial_Delta):
#     # Read data in
#     traces,dimensions,dimensions_nt,trace_len,end_time,delta_time,start_time = read_data(Mode)
#     # Compute difference between traces
#     traces_diff =  compute_diff(traces)

#     # Find time intervals for discrepancy calculations
#     time_intervals, num_ti = find_time_intervals(traces_diff,dimensions_nt,end_time,trace_len,delta_time)

#     # Discrepancy calculation
#     discrepancies = calculate_discrepancies(time_intervals,traces_diff,dimensions_nt,delta_time)

#     return K_value, discrepancies, time_intervals
