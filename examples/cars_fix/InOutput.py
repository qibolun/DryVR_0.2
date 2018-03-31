# Write data to file
def write_to_file(Sim_Result, write_path, type):
    # Write bloat file
    if type == 'simulation':
        with open(write_path, 'w') as write_file:
            for interval in Sim_Result:
                for item in interval:
                    write_file.write(str(item) + ' ')
                write_file.write('\n')




def read_from_file(read_path, type):
	if type == 'simulation':
		trace = []
		with open(read_path, 'r') as trace_file:
			for line in trace_file:
				# Extract data and append to trace
				data = [float(x) for x in line.split()]
				trace.append(data)    
	if type == 'reachtube_single':
		tube = []
		with open(read_path, 'r') as trace_file:
			next(trace_file)
			for line in trace_file:
				# Extract data and append to trace
				data = [float(x) for x in line.split()]
				tube.append(data)    
		return tube
	return trace          

def Reachtube_trunk(reachtube, time_interval):
	reachtube_length = len(reachtube)
	dimensions = len(reachtube[0])
	if reachtube_length % 2 != 0:
		print('Reachtube length is not even, please check!')
		return None


	find_flag = 0
	lower_bound = []
	upper_bound = []
	for i in range(1,dimensions):
		lower_bound.append('nan')
		upper_bound.append('nan')

	for i in range(0, reachtube_length, 2):
		if (reachtube[i][0] >= time_interval[0]) & (reachtube[i][0] <= time_interval[1]):
			if find_flag == 0:
				find_flag = 1
				for dim in range(1,dimensions):
					lower_bound[dim-1] = reachtube[i][dim]
					upper_bound[dim-1] = reachtube[i+1][dim]
			else:
				for dim in range(1,dimensions):
					lower_bound[dim-1] = min(lower_bound[dim-1], reachtube[i][dim])
					upper_bound[dim-1] = max(upper_bound[dim-1], reachtube[i+1][dim])

	# double check output
	for dim in range(1,dimensions):
		if lower_bound[dim-1] > upper_bound[dim-1]:
			print('Find reach set in given time interval is wrong. The computed lower bound is greater than the upper bound!')
			return None

	return lower_bound, upper_bound