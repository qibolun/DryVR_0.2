###########################
# calculate_double_dots:    @input: array (numpy.ndarray)
#                           @output: array (numpy.ndarray)
# - This function calculates the double_dots for the trace. It uses the equation:
# - x_double_dot[t] = (x_dot[t+1] - x_dot[t-1]) / (time[t+1] - time[t-1]).
# - The first term is set to zero as there is no info for this time. For each
# - other timestep between zero and the final timestep, it calculates the change
# - in time and stores it as the denom variable. If denom is zero, there is no
# - useful info and the acceleration for that timestep is set to zero. Otherwise,
# - the acceleration is set using the above equation. Finally, the last value is
# - set to the value previous becuase we cannot use the equation and in general,
# - this is a good approximation for the value. The array with filled in values
# - is returned.
# ---------------------
# - A note on Cython: python code compiled to C code was used because python itself
# - was much too slow. Cython spead up the function by over 100x. In order to
# - use this code you must compile it using the setup.py function. To compile, use
# - the command line call: python setup.py build_ext --inplace
###########################

def calculate_double_dots(array):
    array[0][5] = 0
    array[0][6] = 0

    cdef denom = 0
    for i in range(1, len(array)-1):
        denom = array[i+1][0] - array[i-1][0]
        if denom != 0:
            array[i][5] = (array[i+1][3] - array[i-1][3]) / denom
            array[i][6] = (array[i+1][4] - array[i-1][4]) / denom
        else:
            array[i][5] = 0
            array[i][6] = 0

    array[len(array)-1][5] = array[len(array)-2][5]
    array[len(array)-1][6] = array[len(array)-2][6]
    return array
