# The differential equations of a single car dynamics
#from __future__ import contextlib
from scipy.integrate import odeint
import scipy as scipy

import scipy.special as sc
import numpy as np 
import warnings

def Car_dynamic(y,t,acc,w,mode):
	L = 5.0 # the length of the car, make it fix here
	# make everything double
	acc = float(acc)
	w = float(w)
	# end of making float

	sx, sy, delta, v, psi = y
	#print v
	# psi is the angle between y axis and v
	# y
	# |psi/
	# |  /
	# | /
	# |/__________ x
	sx_dot = v * np.sin(psi)		
	sy_dot = v * np.cos(psi)
	#print "sx_dot: "+str(sx_dot)
	#print "sy_dot: "+str(sy_dot)
	#print "psi: "+str(psi)
	#print "delta: "+str(delta)
	#print "w: "+str(w)

	#print delta

#	if((mode == "Brk") or (mode == "Dec")) and (v < 0):
#		v_dot = 0
#	else:
#		v_dot = acc

	delta_dot = w
	#if(delta>=0.3):
	#	delta_dot=0
	psi_dot = v/L * np.tan(delta)
	#print "v: " + str(v)
	dydt = [sx_dot, sy_dot, delta_dot, acc, psi_dot]
	return dydt


def Car_simulate(Mode,initial,time_bound):
	turntimelimit = 0#TODO Temp solution
	time_step = 0.05;
	time_bound = float(time_bound)
	actualtime = time_bound
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
	# Initialize according to different mode
	if Mode == 'Const':
		acc = 0.0
		w = 0.0
	elif Mode == 'Acc':
		acc = 0.5
		w = 0.0
	elif (Mode == 'Dec') or (Mode == 'Brk'): 
		acc = -0.5
		w = 0.0
	elif Mode =='TurnLeft':
		acc = 0.0
		w = -0.2
		turntimelimit = abs((-0.35-psi_initial))/0.2
		time_bound = min(turntimelimit,time_bound)
		number_points = int(np.ceil(time_bound/time_step))+1
		t = [i*time_step for i in range(0,number_points)]
	elif Mode == 'TurnRight':
		acc = 0.0
		w = 0.2
		turntimelimit = (0.35-psi_initial)/0.2
		time_bound = min(turntimelimit,time_bound)
		number_points = int(np.ceil(time_bound/time_step))+1
		t = [i*time_step for i in range(0,number_points)]
	else:
		print('Wrong Mode name!')

	Initial_ode = [sx_initial, sy_initial, delta_initial, v_initial, psi_initial]
	sol = odeint(Car_dynamic,Initial_ode,t,args=(acc,w,"Const"),hmax = time_step)
	trace = []
	is_zero = False
	turn_lock = False
	max_speed = False
	for j in range(len(t)):
		current_psi = sol[j,4]
		if not is_zero and not turn_lock and not max_speed:
			tmp = []
			tmp.append(t[j])
			tmp.append(sol[j, 0])
			tmp.append(sol[j, 1])
			tmp.append(sol[j, 3] * np.sin(current_psi))
			tmp.append(sol[j, 3] * np.cos(current_psi))
			tmp.append(sol[j, 2])
			trace.append(tmp)

		if((Mode=="Brk") or (Mode=="Dec")) and (sol[j,3]<=0.0) and not is_zero:
			sol[j,3] = 0 
			temp0 = sol[j,0]
			temp1 = sol[j,1]
			temp2 = sol[j,2]
			temp3 = sol[j,3]
			temp4 = sol[j,4]

		if (actualtime>=turntimelimit) and Mode=="TurnRight" and not turn_lock: #this statement needs working if we want to decelerate while driving
			sol[j,2] = 0.35
			temp0 = sol[j, 0]
			temp1 = sol[j, 1]
			temp2 = sol[j, 2]
			temp3 = sol[j, 3]
			temp4 = sol[j, 4]
			turn_lock = True

		if (actualtime>=turntimelimit) and Mode=="TurnLeft" and not turn_lock: #this statement needs working if we want to decelerate while driving
			sol[j,2] = -0.35
			temp0 = sol[j, 0]
			temp1 = sol[j, 1]
			temp2 = sol[j, 2]
			temp3 = sol[j, 3]
			temp4 = sol[j, 4]
			turn_lock = True


		if(abs(sol[j,3])>=45.8 and not max_speed):
			sol[j,3]=45.8
			temp0 = sol[j, 0]
			temp1 = sol[j, 1]
			temp2 = sol[j, 2]
			temp3 = sol[j, 3]
			temp4 = sol[j, 4]
			max_speed = True

		if turn_lock or max_speed:
			
			curtime = t[j]
			Initial_ode = [temp0, temp1, temp2, temp3, temp4]
			time_step = 0.05;
			actualtime = float(actualtime) - curtime
			number_points = int(np.ceil(actualtime / time_step))
			newt = [i * time_step + curtime for i in range(0, number_points)]

			newsol = odeint(Car_dynamic, Initial_ode, newt, args=(0, 0, "Const"), hmax=time_step)
			for x in range(len(newt)):
				tmp1 = []
				tmp1.append(newt[x])
				tmp1.append(newsol[x, 0])
				tmp1.append(newsol[x, 1])
				tmp1.append(newsol[x, 3] * np.sin(newsol[x, 4]))
				tmp1.append(newsol[x, 3] * np.cos(newsol[x, 4]))
				tmp1.append(newsol[x, 2])
				trace.append(tmp1)
			break

		if is_zero:
			tmp.append(t[j])
			tmp.append(temp0)
			tmp.append(temp1)
			tmp.append(temp3*np.sin(temp4))
			tmp.append(temp3*np.cos(temp4))
			tmp.append(temp2)
			trace.append(tmp)
	return trace
