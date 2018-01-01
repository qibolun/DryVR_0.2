# This is file contains wrapper function for c2e2 compiled simulation function
import os

OUTPUTFILE = './output.txt'
CONFILE = './config'
ABSERROR = '1.00000e-10'
REFERROR ='1.00000e-09'

# The config file is in following stanard
# time
# point info dim1
# point info dim2
# ....
# abserror
# referror
# timestep
# timehorizon
# mode num

def invokeSimulator(modeNum, simFile, initial, timeStep, remainTime):
	# Compose the config file
	f = open(CONFILE, 'w')
	# write 0.0 as initial time since we do not have it in DRYVR
	f.write('0.0'+'\n')
	for pt in initial:
		f.write(str(pt) + '\n')

	f.write(ABSERROR+'\n')
	f.write(REFERROR+'\n')
	f.write(str(timeStep)+'\n')
	f.write(str(remainTime)+'\n')
	f.write(str(modeNum))
	f.close()
	commandStr = simFile+ ' <' + CONFILE + ' >' + OUTPUTFILE
	os.system(commandStr)

	# read output file back
	# c2e2 simulator represent simu result as a hyper box
	# we need to get rid of it
	f = open(OUTPUTFILE)
	result = []
	for line in f:
		line = map(float,line.strip().split(' '))
		if not result:
			result.append(line)
		elif line[0] == result[-1][0]:
			continue
		else:
			result.append(line)
	return result

if __name__ == '__main__':
	invokeSimulator(1, './bruss/simu', [2.5, 1.25], 0.01, 10.0)



