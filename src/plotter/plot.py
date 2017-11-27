'''
This file consist main plotter code for DryVR reachtube output
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches

colors = ['red', 'green', 'blue', 'yellow', 'black']

def plot(node, dim, y_min, y_max, xdim):
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
			rect = patches.Rectangle((lb[xdim],lb[d]),ub[xdim]-lb[xdim],ub[d]-lb[d],color=colors[ci%len(colors)],alpha=0.7)
			ax1.add_patch(rect)

	y_axis_min = min([y_min[i] for i in dim])
	y_axis_max = max([y_max[i] for i in dim])
	ax1.set_title(node.nodeId,fontsize=12)
	ax1.set_ylim([y_axis_min, y_axis_max])
	ax1.plot()
	fig1.savefig('output/'+node.fileName+'.png', format='png', dpi=200)


def rrtPlot(lowerBound, upperBound, xDim, yDim, goal, unsafes, region):

	fig1 = plt.figure()
	ax1 = fig1.add_subplot('111')
	x_min = region[0][0]
	y_min = region[0][1]
	x_max = region[1][0]
	y_max = region[1][1]

	# Draw the path
	for i in range(min(len(lowerBound), len(upperBound))):
		lb = map(float, lowerBound[i])
		ub = map(float, upperBound[i])

		rect = patches.Rectangle((lb[xDim], lb[yDim]), ub[xDim]-lb[xDim], ub[yDim]-lb[yDim], color='blue', alpha=0.7)
		ax1.add_patch(rect)

	# Draw the goal
	lb, ub = goal
	rect = patches.Rectangle((lb[0], lb[1]), ub[0]-lb[0], ub[1]-lb[1], color='green', alpha=0.7)
	ax1.add_patch(rect)

	# Draw the unsafe
	for unsafe in unsafes:
		lb, ub = unsafe
		rect = patches.Rectangle((lb[0], lb[1]), ub[0]-lb[0], ub[1]-lb[1], color='red', alpha=0.7)
		ax1.add_patch(rect)

	ax1.set_title("RRT",fontsize=12)
	ax1.set_ylim([y_min, y_max])
	ax1.set_xlim([x_min, x_max])
	ax1.plot()
	fig1.savefig('output/rrt.png', format='png', dpi=200)
