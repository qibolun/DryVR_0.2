from Car_Dynamic_Single import Car_simulate
import numpy as np

x = [16.67, 4.17, 30.0, 20.0, 25.0, 10.0,8.0,5.0,3.0,27.5,17.5,2,12.5,1]
y = [0.014,0.22,0.0043,0.0097,0.0061,0.039,0.069,0.155,0.43,0.0052,0.0125,0.97,0.025,4.03]

lookuptable = {}
for idx,val in enumerate(x):
	lookuptable[val] = y[idx]

# for key in sorted(lookuptable):
# 	print key, lookuptable[key]

line = np.linspace(1.0, 30.0, 290, endpoint = False)



def searchSpeed(lb,ub,speed):
	while lb+0.0001 < ub:
		mid = (ub+lb)/2
		trace = Car_simulate("TurnLeft", [0.0,0.0,0.0,speed], "10", mid)
		if abs(-trace[-1][1]-3) <= 0.02:
			return mid
		elif -trace[-1][1]-3>0.02:
			ub = mid
		else:
			lb = mid
	return -1


print sorted(lookuptable.keys())
for val in line:
	if val in lookuptable:
		continue

	keys = sorted(lookuptable.keys())
	lb = 0.0043
	ub = 4.03
	for i in range(len(keys)-1):
		if val > keys[i] and val < keys[i+1]:
			lb = lookuptable[keys[i+1]]
			ub = lookuptable[keys[i]]
	result = searchSpeed(lb,ub,val)
	if result == -1:
		print("something is wrong with speed", val)
		continue

	lookuptable[val] = result
retkey = []
retval = []
for key in sorted(lookuptable):
	retkey.append(key)
	retval.append(lookuptable[key])

print retkey,retval