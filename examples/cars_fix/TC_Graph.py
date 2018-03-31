from igraph import *

def takeOverGraph():
	g = Graph(directed = True)
	g.add_vertices(6)
	g.add_edges([(0,1),(1,2),(2,3),(3,4),(4,5)])
	transtime =[(5,6),(10,12),(5,6),(5,6),(10,12)]
	divid_intervals = [2,1,1,1,2]
	if g.is_dag()==True:
		print("Graph provided is a DAG")
	else:
		print("Graph provided is not a DAG, quit()")
	g.vs["label"] = [("Acc1;Const"),("TurnLeft;Const"),("Acc2;Const"),
	("Dec;Const"),("TurnRight;Const"),("Const;Const")]
	# g.vs["label"] = [("Acc1;Const"),("TurnRight;Const"),("Acc2;Const")]
	g.vs["name"] = g.vs["label"]
	#edges_labels = [str(t) for t in transtime]
	g.es["label"] = transtime
	g.es["trans_time"] = transtime
	g.es["divid"] = divid_intervals
	PT_Pic = plot(g,"CarOverTake.png",margin=40)
	PT_Pic.save()
	#print("The structure of the powertrain graph has been saved in the folder as a .png picture")
	return g

def carOneGraph():
	g = Graph(directed = True)
	g.add_vertices(12)
	g.add_edges([(0,1),(1,2),  (2,3),(3,4),(4,5),  (1,6),  (6,7),(7,8),  (8,5),  (1,9),  (9,10),(10,11),(11,5)])
	transtime = [(5,6),(10,12),(5,6),(5,6),(10,12),(10,12),(5,6),(14,16),(10,12),(10,12),(5,6), (5,6),  (10,12)]
	divid_intervals = [1,1,1,1,1,1,1,1,1,1,1,1,1]

	if g.is_dag()==True:
		print("Graph provided is a DAG")
	else:
		print("Graph provided is not a DAG, quit()")

	#layout = g.layout("kk")
	g.vs["label"] = [("Acc1;Const"),("TurnLeft;Const"),("Acc2;Const"),
	("Dec;Const"),("TurnRight;Const"),("Const;Const"),("Acc1;Acc1"),
	("Dec;Acc1"),("TurnRight;Acc1"),("Acc1;Dec"),("Const;Dec"),("TurnRight;Const")]
	g.vs["name"] = g.vs["label"]
	#edges_labels = [str(t) for t in transtime]
	g.es["label"] = transtime
	g.es["trans_time"] = transtime
	g.es["divid"] = divid_intervals
	PT_Pic = plot(g,"Car.png",margin=40)
	PT_Pic.save()
	#print("The structure of the powertrain graph has been saved in the folder as a .png picture")
	return g

def mergeGraph():
	g = Graph(directed = True)
	g.add_vertices(7)
	g.add_edges([(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,4)])
	transtime=[(1,2),(5,6),(5,6),(10,12),(1,2),(5,6),(10,12)]
	divid_intervals = [1,1,1,1,1,1,1]

	if g.is_dag()==True:
		print("Graph provided is a DAG")
	else:
		print("Graph provided is not a DAG, quit()")

	g.vs["label"] = [("Const;Const"),("Acc1;Acc1"),("Dec;Acc1"),
	("TurnRight;Const"),("Const;Const"),("Acc1;Const"),('TurnRight;Const')]
	g.vs["name"] = g.vs["label"]
	g.es["label"] = transtime
	g.es["trans_time"] = transtime
	g.es["divid"] = divid_intervals
	PT_Pic = plot(g,"Car2.png",margin=40)
	PT_Pic.save()

	return g


def mergeGraphSimple():
	g = Graph(directed = True)
	g.add_vertices(4)
	g.add_edges([(0,1),(1,2),(2,3)])
	transtime=[(1,2),(5,6),(5,6),(10,12),(1,2),(5,6),(10,12)]
	divid_intervals = [1,1,1,1,1,1,1]

	if g.is_dag()==True:
		print("Graph provided is a DAG")
	else:
		print("Graph provided is not a DAG, quit()")

	g.vs["label"] = [("Const;Const"),("Acc1;Const"),("TurnRight;Const"),("Const;Const")]
	g.vs["name"] = g.vs["label"]
	g.es["label"] = transtime
	g.es["trans_time"] = transtime
	g.es["divid"] = divid_intervals
	PT_Pic = plot(g,"Car2.png",margin=40)
	PT_Pic.save()

	return g
