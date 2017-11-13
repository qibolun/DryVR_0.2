# The differential equations of a single car dynamics

from scipy.integrate import odeint
import numpy as np 

def Car_dynamic(y,t,acc,w,mode):
	L = 5.0 # the length of the car, make it fix here
	# make everything double
	acc = float(acc)
	w = float(w)
	# end of making float

	sx, sy, delta, v, psi = y
	# psi is the angle between y axis and v
	# y
	# |psi/
	# |  /
	# | /
	# |/__________ x
	sx_dot = v * np.sin(psi)		
	sy_dot = v * np.cos(psi)
	#print delta
	if abs(delta) > 0.216 :
		delta_dot = 0
	else: 
		delta_dot = w
	if((mode == "Brk") or (mode == "Dec")) and (v < 0):
		v_dot = 0
	else: 
		v_dot = acc
	psi_dot = v/L * np.tan(delta)
	dydt = [sx_dot, sy_dot, delta_dot, v_dot, psi_dot]
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
	if vy_initial == 0:
		psi_initial = np.pi/2
	else:
		psi_initial = np.arctan(vx_initial/vy_initial)
	delta_initial = initial[4]	# magic number

	v_initial = (vx_initial**2 + vy_initial**2)**0.5
	acc = 0.0
	acc_time = 0.0
	turn_time = 0.0
	turn_back_time = 0.0
	#print "begin"
	# Initialize according to different mode
	if Mode == 'Const':
		acc = 0.0
		w = 0.0
	elif Mode == 'Acc':
		acc = 0.2
		w = 0.0
	elif (Mode == 'Dec') or (Mode == 'Brk'): 
		acc = -0.2
		w = 0.0
	elif Mode =='TurnLeft':
		acc = 0.0
		w = -0.5
	elif Mode == 'TurnRight':
		acc = 0.0
		w = 0.5
	else:
		print('Wrong Mode name!')

	Initial_ode = [sx_initial, sy_initial, delta_initial, v_initial, psi_initial]
	sol = odeint(Car_dynamic,Initial_ode,t,args=(acc,w,Mode),hmax = time_step)

	# Construct the final output
	trace = []
	for j in range(len(t)):
		current_psi = sol[j,4]
		#print t[j], current_psi
		tmp = []
		tmp.append(t[j])
		tmp.append(sol[j,0])
		tmp.append(sol[j,1])
		tmp.append(sol[j,3]*np.sin(current_psi))
		tmp.append(sol[j,3]*np.cos(current_psi))
		tmp.append(sol[j,2])
		trace.append(tmp)
	return trace
