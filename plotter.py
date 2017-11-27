import argparse
import pygraphviz as pgv

from src.plotter.parser import parse
from src.plotter.plot import plot

parser = argparse.ArgumentParser(
	description = 'This is plotter script for DryVR generated reach tube output'
)

parser.add_argument('-f', type=str, default='output/reachtube.txt', help='file path for reach tube')
parser.add_argument('-y', type=str, default='[1]', help='dimension number you want to plot, ex [1,2], default first dimension')
parser.add_argument('-x', type=str, default='0', help='dimension number you want to plot, ex 0, default time')
parser.add_argument('-o', type=str, default='plotResult.png', help='output file name')
args = parser.parse_args()

try:
	file = open(args.f, 'r')
except IOError:
	print ('File does not exist')

lines = file.readlines()
initNode, y_min, y_max= parse(lines)

ydim = eval(args.y)
xdim = eval(args.x)
# Using DFS algorithm to Draw image per Node
stack = [initNode]
while stack:
	curNode = stack.pop()
	for c in curNode.child:
		stack.append(curNode.child[c])
	plot(curNode, ydim, y_min, y_max, xdim)

# Construct node graph
G=pgv.AGraph(strict=True, directed=True)

# Using DFS algorithm to add node and egde of the graph
G.add_node(initNode.fileName, image='output/'+initNode.fileName+'.png')
stack = [initNode]
while stack:
	curNode = stack.pop()
	for c in curNode.child:
		childNode = curNode.child[c]
		G.add_node(childNode.fileName, image='output/'+childNode.fileName+'.png')
		G.add_edge(curNode.fileName, childNode.fileName)
		stack.append(childNode)
G.layout(prog='dot')
G.draw(args.o)  # write previously positioned graph to PNG file
