'''
This file consist main plotter code for DryVR reachtube output
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches

colors = ['red', 'green', 'blue', 'yellow', 'black']

def plot(node, dim, y_min, y_max):
	fig1 = plt.figure()
	ax1 = fig1.add_subplot('111')
	lowerBound = []
	upperBound = []
	for key in sorted(node.lowerBound):
		lowerBound.append(node.lowerBound[key])
	for key in sorted(node.upperBound):
		upperBound.append(node.upperBound[key])

	for i in range(min(len(lowerBound),len(upperBound))):
		lb = map(float,lowerBound[i])
		ub = map(float,upperBound[i])
		#print lb[0],ub[0], lb[1],ub[1]

		for ci, d in enumerate(dim):
			rect = patches.Rectangle((lb[0],lb[d]),ub[0]-lb[0],ub[d]-lb[d],color=colors[ci%len(colors)],alpha=0.7)
			ax1.add_patch(rect)

	y_axis_min = min([y_min[i] for i in dim])
	y_axis_max = max([y_max[i] for i in dim])
	ax1.set_title(node.nodeId,fontsize=12)
	ax1.set_ylim([y_axis_min, y_axis_max])
	ax1.plot()
	fig1.savefig('output/'+node.fileName+'.png', format='png', dpi=200)


