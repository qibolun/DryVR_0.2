from Car_Dynamic_Single import *


def TC_Simulate(Modes,initialCondition,time_bound):
	Modes = Modes.split(';')
	num_cars = len(Modes)
	#print initialCondition

	if len(initialCondition) == 4*num_cars:
		for car_numer in range(num_cars):
			Current_Initial = initialCondition[car_numer*4:car_numer*4+4]
			trace = Car_simulate(Modes[car_numer],Current_Initial,time_bound)
			trace = np.array(trace)
			if car_numer == 0:
				Final_trace = np.zeros(trace.size)
				Final_trace = trace
			else:
				Final_trace = np.concatenate((Final_trace, trace[:,1:5]), axis=1)
	else:
		print('Number of cars does not match the initial condition')

	return Final_trace
