
from scipy.integrate import odeint
import numpy as np 

def robot_dynamic(y, t, xrate, yrate):
	dydt = [xrate, yrate]
	return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
	time_step = 0.05;
	time_bound = float(time_bound)
	
	number_points = int(np.ceil(time_bound/time_step))
	t = [i*time_step for i in range(0,number_points)]
	if t[-1] != time_step:
		t.append(time_bound)
	newt = []
	for step in t:
		newt.append(float(format(step, '.2f')))
	t = newt
 	
	x_initial = initialCondition[0]
	y_initial = initialCondition[1]

	xrate = 0.0
	yrate = 0.0
	if Mode == 'UP':
		xrate = -1
	elif Mode == 'DOWN':
		xrate = 1
	elif Mode == 'LEFT':
		yrate = -1
	elif Mode == 'RIGHT':
		yrate = 1
	else:
		print('Wrong Mode name!')
	sol = odeint(robot_dynamic,initialCondition,t,args=(xrate,yrate),hmax = time_step)

	# Construct the final output
	trace = []
	for j in range(len(t)):
		#print t[j], current_psi
		tmp = []
		tmp.append(t[j])
		tmp.append(float(sol[j,0]))
		tmp.append(float(sol[j,1]))
		trace.append(tmp)
	return trace

if __name__ == "__main__":
	sol = TC_Simulate('RIGHT',[0.0,0.0],5)
	for s in sol:
		print(s)