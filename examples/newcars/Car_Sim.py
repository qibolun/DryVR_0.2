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
				if len(trace)!=len(Final_trace):
					print len(trace), len(Final_trace)
					for i in range(min(len(trace), len(Final_trace))):
						print trace[i][0], Final_trace[i][0]
					print Final_trace
				Final_trace = np.concatenate((Final_trace, trace[:,1:6]), axis=1)
	else:
		print('Number of cars does not match the initial condition')

	return Final_trace

if __name__ == "__main__":

	sol = TC_Simulate("Dec", [0, 0, 0, 1, 0.0], 30)
	# for line in sol:
	# 	print line
	#nextsol = TC_Simulate("TurnRight",sol[-1][1:],50)#2.4

	#finalsol = TC_Simulate("Const",nextsol[-1][1:],1.5)
	#print sol
	#for i in sol:
	#	print i
	#for j in nextsol:
	#	print j

	#nextsoltime = [(row[0]+sol[-1][0]) for row in nextsol]
	#sxnext = [row[1] for row in nextsol]
	#synext = [row[2] for row in nextsol]
	sx = [row[1] for row in sol]
	sy = [row[2] for row in sol]
	#sxfinal = [row[1] for row in finalsol]
	#syfinal = [row[2] for row in finalsol]
	# plt.plot(sx, sy, "-r")
	# plt.show()

	# 	nextdelta = [row[5] for row in nextsol]
# #	for row in sol:
# #		print row
# 	#print "NEXTSOL"
# 	#for row in nextsol:
# #		print row
# 	time = [row[0] for row in sol]
# 	vx = [row[3] for row in sol]
# 	vy = [row[4] for row in sol]
# 	delta = [row[5] for row in sol]
	#plt.plot(time,sx,"-r")
	#plt.plot(time,sy,"-g")
	#plt.plot(time,vx,"-k")
	#plt.plot(time,vy,"-y")
	# plt.plot(time,delta,"-b")
	# plt.show()

	# plt.plot(nextsoltime,nextdelta)
	# plt.show()
