
from scipy.integrate import odeint
import numpy as np 

def thermo_dynamic(y,t,rate):
	dydt = rate*y
	return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
	time_step = 0.05;
	time_bound = float(time_bound)
	initial = [float(tmp)  for tmp in initialCondition]
	number_points = int(np.ceil(time_bound/time_step))
	t = [i*time_step for i in range(0,number_points)]
	if t[-1] != time_step:
		t.append(time_bound)

	y_initial = initial[0]

	if Mode == 'On':
		rate = 0.1
	elif Mode == 'Off':
		rate = -0.1
	else:
		print('Wrong Mode name!')
	sol = odeint(thermo_dynamic,y_initial,t,args=(rate,),hmax = time_step)

	# Construct the final output
	trace = []
	for j in range(len(t)):
		#print t[j], current_psi
		tmp = []
		tmp.append(t[j])
		tmp.append(sol[j,0])
		trace.append(tmp)
	return trace


# sol = TC_Simulate('Off',[60],10)
# print(sol)