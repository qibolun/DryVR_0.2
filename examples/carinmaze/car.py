
from scipy.integrate import odeint
from math import cos, sin, pi
import numpy as np 

def robot_dynamic(y, t, Mode):
	desired_velocity = [sin(Mode * pi/4), cos(Mode * pi/4)]
	px, py, vx, vy = y
	difvx = vx-desired_velocity[0]
	difvy = vy-desired_velocity[1]
	vx_dot = -1.8 * difvx + 0.1*difvy
	vy_dot = 0.1 * difvx - 1.8*difvy
	px_dot = vx
	py_dot = vy
	dydt = [px_dot, py_dot, vx_dot, vy_dot]
	return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
	time_step = 0.01;
	time_bound = float(time_bound)
	
	number_points = int(np.ceil(time_bound/time_step))
	t = [i*time_step for i in range(0,number_points)]
	if t[-1] != time_step:
		t.append(time_bound)
	newt = []
	for step in t:
		newt.append(float(format(step, '.2f')))
	t = newt


	sol = odeint(robot_dynamic,initialCondition,t,args=(float(Mode),),hmax = time_step)

	# Construct the final output
	trace = []
	for j in range(len(t)):
		#print t[j], current_psi
		tmp = []
		tmp.append(t[j])
		tmp.append(float(sol[j,0]))
		tmp.append(float(sol[j,1]))
		tmp.append(float(sol[j,2]))
		tmp.append(float(sol[j,3]))
		trace.append(tmp)
	return trace

if __name__ == "__main__":
	sol = TC_Simulate('3',[0.0,0.0,1.0,0.0],5)
	for s in sol:
		print(s)