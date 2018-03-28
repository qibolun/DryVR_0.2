# The differential equations of a single car dynamics

from scipy.integrate import odeint
import numpy as np 

def Car_dynamic(y,t,v_initial,acc,acc_time,turn_indicator,turn_time,turn_back_time):
	L = 5.0 # the length of the car, make it fix here
	# make everything double
	v_initial = float(v_initial)
	acc = float(acc)
	y = [float(tmp) for tmp in y]
	acc_time = float(acc_time)
	turn_time = float(turn_time)
	turn_back_time = float(turn_back_time)
	# end of making float

	# set the velocity
	if t <= acc_time:
		v = v_initial
		#print('20')
	elif (t > acc_time) and (t <= acc_time + 5.0):
		v = v_initial + acc*(t-acc_time)
		#print('23')
	elif t > acc_time + 5.0:
		v = v_initial + acc * 5.0
		#print('25')
	else:
		print('Something is wrong with time here when calculting velocity!')
	# set the steering angle
	delta_initial = 0.0
	if turn_indicator == 'Right':
		# print(t)
		if t <= turn_time:
			delta_steer = delta_initial;
		elif (t > turn_time) and (t <= turn_time + 2.0):
			delta_steer = delta_initial + 1.0 
		elif (t > turn_time + 2.0) and (t <= turn_back_time):
			delta_steer = delta_initial 
		elif (t > turn_back_time) and (t <= turn_back_time + 2.0):
			delta_steer = delta_initial - 1.0 
		elif t > turn_back_time + 2.0:
			delta_steer = delta_initial
		else:
			print('Something is wrong with time here when calculting steering angle!')
	elif turn_indicator =='Left':
		if t <= turn_time:
			delta_steer = delta_initial;
		elif (t > turn_time) and (t <= turn_time + 2.0):
			delta_steer = delta_initial + (-1.0) 
		elif (t > turn_time + 2.0) and (t <= turn_back_time):
			delta_steer = delta_initial 
		elif (t > turn_back_time) and (t < turn_back_time + 2.0):
			delta_steer = delta_initial + (1.0)
		elif t > turn_back_time + 2.0:
			delta_steer = delta_initial
		else:
			print('Something is wrong with time here when calculting steering angle!')
	elif turn_indicator == 'Straight':
		delta_steer = delta_initial
	else:
		print('Wrong turn indicator!')

	psi, sx, py = y
	psi_dot = (v)/L*(np.pi/8.0)*delta_steer
	w_z = psi_dot
	sx_dot = v * np.cos(psi) - L/2.0 * w_z * np.sin(psi) 
	sy_dot = v * np.sin(psi) + L/2.0 * w_z * np.cos(psi)
	#sx_dot = v * np.cos(psi) 
	#sy_dot = v * np.sin(psi)
	dydt = [psi_dot, sx_dot, sy_dot]
	return dydt


def Car_simulate(Mode,initial,time_bound):
	time_step = 0.05;
	time_bound = float(time_bound)
	initial = [float(tmp)  for tmp in initial]
	number_points = int(np.ceil(time_bound/time_step))
	t = [i*time_step for i in range(0,number_points)]
	if t[-1] != time_step:
		t.append(time_bound)

	# initial = [sx,sy,vx,vy]
	# set the parameters according to different modes
	# v_initial,acc,acc_time,turn_indicator,turn_time,turn_back_time

	sx_initial = initial[0]
	sy_initial = initial[1]
	vx_initial = initial[2]
	vy_initial = initial[3]
	psi_initial = 1.0*(-np.pi/2)

	v_initial = (vx_initial**2 + vy_initial**2)**0.5
	acc = 0.0
	acc_time = 0.0
	turn_time = 0.0
	turn_back_time = 0.0

	# Initialize according to different mode
	if Mode == 'Const':
		turn_indicator = 'Straight'
	elif ((Mode == 'Acc1') or (Mode == 'Acc2')):
		turn_indicator = 'Straight'
		acc = 0.2
		acc_time = 0.0
	elif (Mode == 'Dec') or (Mode == 'Brk'): 
		turn_indicator = 'Straight'
		if v_initial == 0.0:
			acc = 0.0
		else:
			acc = -0.2
		acc_time = 0.0
	elif Mode =='TurnLeft':
		turn_indicator = 'Left'
		turn_time = 0.0
		turn_back_time = 5.0
	elif Mode == 'TurnRight':
		turn_indicator = 'Right'
		turn_time = 0.0
		turn_back_time = 5.0
	else:
		print('Wrong Mode name!')

	Initial_ode = [psi_initial, sx_initial, sy_initial]
	sol = odeint(Car_dynamic,Initial_ode,t,args=(v_initial,acc,acc_time,turn_indicator,turn_time,turn_back_time),hmax = time_step)

	# Construct v
	v = np.zeros(len(t))

	for i in range(len(t)):
		if t[i] <= acc_time:
			v[i] = v_initial
		elif (t[i] > acc_time) and (t[i] <= acc_time + 5.0):
			v[i] = v_initial + acc*(t[i]-acc_time)
		elif (t[i] > acc_time + 5.0):
			v[i] = v_initial + acc * 5.0


	# Construct the final output
	trace = []
	for j in range(len(t)):
		current_psi = sol[j,0]
		#print t[j], current_psi
		tmp = []
		tmp.append(t[j])
		tmp.append(sol[j,1])
		tmp.append(sol[j,2])
		tmp.append(v[j]*np.cos(current_psi))
		tmp.append(v[j]*np.sin(current_psi))
		trace.append(tmp)
	return trace