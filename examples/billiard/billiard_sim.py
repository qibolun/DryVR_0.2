from billiard_single import *

def TC_Simulate(Modes,initialCondition,time_bound):
	Modes = Modes.split(';')
	num_balls = len(Modes)
	#print initialCondition

	if len(initialCondition) == 4*num_balls:
		for ball_number in range(num_balls):
			Current_Initial = initialCondition[ball_number*4:ball_number*4+4]
			trace = Ball_simulate(Modes[ball_number],Current_Initial,time_bound)
			trace = np.array(trace)
			if ball_number == 0:
				Final_trace = np.zeros(trace.size)
				Final_trace = trace
			else:
				Final_trace = np.concatenate((Final_trace, trace[:,1:5]), axis=1)
	else:
		print('Number of balls does not match the initial condition')

	return Final_trace
if __name__ == "__main__":
    trace = TC_Simulate("normal", [0,0,1,1], 5)
    print trace

    trace = TC_Simulate("normal;normal", [0,0,1,0,0,0,0,1], 5)
    print trace
