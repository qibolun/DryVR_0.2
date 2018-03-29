import random
from InOutput import *
from igraph import *
from Car_Sim import *



def simulate(g,initialCondition,Time_horizon):
	Compute_Order = g.topological_sorting(mode=OUT)
	Current_Vertex = Compute_Order[0]


	remainTime = Time_horizon
	# eng = matlab.engine.start_matlab()
	# print('Matlab Started!')
	# eng.setup(nargout=0)
	Current_Time = 0




	dimensions = len(initialCondition)+1


	simResult = []

	while remainTime>0:
		print '-----------------------------------------------------'
		print 'Current State', g.vs[Current_Vertex]['label']

		Current_successors = g.successors(Current_Vertex)
		if len(Current_successors)==0:
			Transite_Time = remainTime
			print("Last mode, no more transitions, will stop at %f second" % (Transite_Time))
		else:
			Current_Successor = random.choice(Current_successors)
			edgeid = g.get_eid(Current_Vertex,Current_Successor)
			Current_transtime = g.es[edgeid]["label"]
			Transite_Time = float(random.uniform(Current_transtime[0],Current_transtime[1]))
			print("Will transite to mode %s at %f second" % (g.vs[Current_Successor]["label"], Transite_Time))

		curLabel = g.vs[Current_Vertex]['label']

		Current_Simulation = TC_Simulate(curLabel,initialCondition,Transite_Time)
		


		for i in range (len(Current_Simulation)):
			Current_Simulation_row = [Current_Simulation[i][0] + Current_Time]
			for j in range (1,len(Current_Simulation[0])):
				Current_Simulation_row.append(Current_Simulation[i][j])
			simResult.append(Current_Simulation_row)

		#simResult+=Current_Simulation
		remainTime-=Transite_Time
		initialCondition = Current_Simulation[-1][1:]
		Current_Time = Current_Time + Transite_Time

		Current_Vertex = Current_Successor

	return simResult
	#write_to_file(simResult,'output/TC_Traj.txt','simulation')

	


