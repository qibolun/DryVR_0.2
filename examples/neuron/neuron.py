from oct2py import octave
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
octave.addpath(dir_path)
def TC_Simulate(Mode,initialCondition,time_bound):
	ret = octave.neuronSim(initialCondition, time_bound)

	return list(ret)

if __name__ == "__main__":
	ret = TC_Simulate("default", [-0.0280794, -0.0280874, -0.0337083, -0.0280171, -0.0272915, -0.0337002, -0.0161361, -0.0091623, -0.0239873], 0.06)
	print ret
