from Car_Dynamic_Single import *
import matplotlib.pyplot as plt

def TC_Simulate(Modes,initialCondition,time_bound):
	Modes = Modes.split(';')
	num_cars = len(Modes)
	#print initialCondition

	if len(initialCondition) == 5*num_cars:
		for car_numer in range(num_cars):
			Current_Initial = initialCondition[car_numer*5:car_numer*5+5]
			trace = Car_simulate(Modes[car_numer],Current_Initial,time_bound)
			trace = np.array(trace)
			if car_numer == 0:
				Final_trace = np.zeros(trace.size)
				Final_trace = trace
			else:
				Final_trace = np.concatenate((Final_trace, trace[:,1:6]), axis=1)
	else:
		print('Number of cars does not match the initial condition')

	return Final_trace

if __name__ == "__main__":

	sol = TC_Simulate("TurnLeft", [0, 0, 0, 1, 0], 50.0)
	#for s in sol:
	#	print s
	time = [row[0] for row in sol]
	sx = [row[1] for row in sol]
	sy = [row[2] for row in sol]
	vx = [row[3] for row in sol]
	vy = [row[4] for row in sol]
	delta = [row[5] for row in sol]
	plt.plot(time,sx,"-r")
	plt.plot(time,sy,"-g")
	plt.plot(time,vx,"-k")
	plt.plot(time,vy,"-y")
	plt.plot(time,delta,"-b")
	plt.show()
	plt.plot(sx, sy, "-r")
	plt.show()

	

