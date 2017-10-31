from Car_Dynamic_Single import *


def TC_Simulate(Modes,initialCondition,time_bound):
	# For this model, we are giving relative values such as 
	# sx,sy,vx,vy
	# There will be a single model but we consider that y is a car that always move
	# with y = 1


	Current_Initial = initialCondition
	trace = Car_simulate(Modes,Current_Initial,time_bound)
	return trace



def main():
	t = TC_Simulate("TurnLeft", [0,15,0,0], 10)
	for line in t:
		print line
if __name__ == "__main__":
	main()

