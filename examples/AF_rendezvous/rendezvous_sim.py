###########################
######### Imports #########
###########################
import matlab.engine
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import os

###########################
##### Cython Imports ######
###########################
import pyximport; pyximport.install()
from acceleration import calculate_double_dots

###########################
####### Variables #########
###########################
COLUMNS         = ['time', 'x', 'y', 'x_dot', 'y_dot']
FULL_COLUMNS    = ['time', 'x', 'y', 'x_dot', 'y_dot', 'x_double_dot', 'y_double_dot', 'force_x', 'force_y']

mu          = 3.986e14 # m^3 / s^2
r_0         = 7.1e6 # m
n           = np.sqrt(mu/r_0**3)
m_chaser    = 500 # kg
m_target    = 2000 # kg

###########################
# compact_trace:    @input: arr (numpy.ndarray), compact factor (int)
#                   @output: compacted trace (numpy.ndarray)
# - This function takes in a trace and a compact factor. It uses
# - numpy splice notation to select each entry from the array with a
# - step size of compact_factor and returns the new array.
###########################
def compact_trace(arr, compact_factor):
    return arr[::compact_factor]

###########################
# generate_trace:   @input: curLabel (str), initCondition (list), transiteTime (int)
#                   @output: trace (numpy.ndarray)
# - This function starts a matlab session using the python matlab engine.
# - It then calls the matlab.engine.Simulate function. This function is
# - defined where the matlab.engine.addpath call points. It is defined by
# - the name of the file. The inputs to this function need to be altered to
# - meet the matlab format. The matlab code will generate a traces consiting
# - of a series of vectors containing [x, y, x_dot, y_dot] data. Since only
# - 4 values are calculated, only the first 4 initial conditions are passed.
# - The trace is returned as a numpy.ndarray
###########################
def generate_trace(curLabel, initCondition, transiteTime):
    eng = matlab.engine.start_matlab()
    path = os.path.abspath(os.path.dirname(__file__))+'/matlabcode'

    eng.addpath(path)
    sim_data = eng.Simulate(    curLabel,
                                matlab.double(initCondition[0:4]),
                                float(transiteTime)
    )
    return np.array(sim_data)

###########################
# add_variables:    @input: arr (numpy.ndarray)
#                   @output: arr (numpy.ndarray)
# - This function creates a new numpy.ndarray of zeros with same number of rows
# - as the input array and 4 columns to represent computed variables. The final
# - data will include: [x, y, x_dot. y_dot, x_double_dot, y_double_dot, force_x, force_y].
# - The new array is appended to the input array and returned.
###########################
def add_variables(arr):
    temp = np.zeros((arr.shape[0], 4))
    return np.append(arr, temp, axis=1)

###########################
# calculate_acceleration:   @input: arr (numpy.ndarray)
#                           @output: arr (numpy.ndarray)
# This function calculates the acceleration (double_dot) values for each
# timestep of an input array. It calls python code that has been compiled
# down to C for speed. It outputs the same array with double_dot values
# filled in.
###########################
def calculate_acceleration(arr):
    return calculate_double_dots(arr)

###########################
# find_min_index:   @input: arr (numpy.ndarray)
#                   @output: min_index (int)
# - This function finds the minimum index for the position of chaser spacecraft
# - in relation to the target spacecraft. This calculation is referred to as "rho"
# - which is defined as rho(x,y) = sqrt(x^2 + y^2). For each timestep in the trace
# - the function computes rho and compares it to the current minimum value seen.
# - Once it goes through the entire trace, it returns the index where the
# - minimum value occured.
###########################
def find_min_index(arr):
    min_val = float('Inf')
    min_index = None
    for i in range(arr.shape[0]):
        rho = np.sqrt(arr[i][1]**2 + arr[i][2]**2)
        if rho < min_val:
            min_val = rho
            min_index = i
    return min_index

###########################
# calculate_forces:     @input: arr (numpy.ndarray)
#                       @output: arr (numpy.ndarray)
# - This function take in a trace in the form of a numpy.ndarray. It works in two
# - steps: before rendezvous and after rendezvous. First, the min_index is found
# - using the find_min_index function. Next, for each timestep in the trace,
# - there is a check to see if it is the minimum index. If not, the trace is in
# - before rendezvous state. It calculates the force in the x and y direction as
# - it was stated in the research paper. If the index is the minimum found, the
# - chaser and target are as close as they will ever be and it can be assumed that
# - the rendezvous has occured. Since we no longer want to check this, the check
# - variable is set to false. We then add the mass of the target to the mass used
# - in calculating the force. Finally we use F = ma to calculate the force.
# - The array with filled in values for force is returned.
###########################
def calculate_forces(arr):
    m = m_chaser
    min_index = find_min_index(arr)
    check = True
    for i in range(arr.shape[0]):
        if check:
            if i == min_index:
                check = False
                m += m_target
                arr[i][7] = m * arr[i][5]
                arr[i][8] = m * arr[i][6]
            else:
                arr[i][7] = m * (arr[i][5] - 2*n*arr[i][4] - 3*n*n*arr[i][1])
                arr[i][8] = m * (arr[i][6] + 2*n*arr[i][3])
        else:
            arr[i][7] = m * arr[i][5]
            arr[i][8] = m * arr[i][6]
    return arr

###########################
# plot_total_force:     @input: arr (numpy.ndarray)
#                       @output: None
# - This function plots the total force vs time as a scatter plot. It was
# - used as debugging tool.
###########################
def plot_total_force(arr):
    df = pd.DataFrame(arr, columns=FULL_COLUMNS)
    force = np.sqrt(df['force_x']*df['force_x'] + df['force_y']*df['force_y'])
    plt.scatter(df['time'], force, s=1)
    plt.show()

###########################
# TC_Simulate:      @input: curLabel (str), initCondition (list), transiteTime (int)
#                   @output: arr (numpy.ndarray)
# - This is the function called by DryVR. It contains print statements and timing
# - that is provide to the user of DryVR. The main steps taken in this function:
# -     1) generate_trace
# -     2) add_variables (that are values of zero i.e. placeholders)
# -     3) calculate_acceleration
# -     4) compact_trace (done before adding force for runtime efficiencies)
# -     5) calculate_forces
# -     6) return trace
# - Each step is timed so that it is obvious what the limiting functions are.
###########################
def TC_Simulate(curLabel, initCondition, transiteTime):
    print "\n~~~ Starting Simulation ~~~"
    start = dt.datetime.now()

    time = dt.datetime.now()
    arr = generate_trace(curLabel, initCondition, transiteTime)
    print '\tGenerated Trace:', (dt.datetime.now() - time).total_seconds() * 1000, 'ms'

    time = dt.datetime.now()
    arr = add_variables(arr)
    print '\tAdded Variables:', (dt.datetime.now() - time).microseconds / 1000, 'ms'

    time = dt.datetime.now()
    arr = calculate_acceleration(arr)
    print '\tCalculated Acceleration:', (dt.datetime.now() - time).microseconds / 1000, 'ms'

    time = dt.datetime.now()
    arr = compact_trace(arr, 100)
    print '\tCompacted Trace:', (dt.datetime.now() - time).microseconds / 1000, 'ms'

    time = dt.datetime.now()
    arr = calculate_forces(arr)
    print '\tCalculated Forces:', (dt.datetime.now() - time).microseconds / 1000, 'ms'

    print "Completed:", (dt.datetime.now() - start).total_seconds() * 1000, 'ms'
    print "Trace Length:", len(arr)
    return arr
