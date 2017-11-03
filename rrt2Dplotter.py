import argparse

from src.plotter.parser import parse
from src.plotter.plot import rrtPlot
parser = argparse.ArgumentParser(
	description = 'This is plotter script for DryVR generated reach tube output'
)
parser.add_argument('-f', type=str, default='output/rrtTube.txt', help='file path for reach tube')
parser.add_argument('-d', type=str, default='[1, 2]', help='dimension number for x, y, ex [1,2]')

args = parser.parse_args()

try:
	file = open(args.f, 'r')
except IOError:
	print ('File does not exist')

goal = [[3.0,3.0],[4.0,4.0]]
unsafes = [[[2.0, 3.0],[3.0,4.0]], [[3.0,2.0],[4.0,3.0]]]
regions = [[0,0],[5,5]]

dim = eval(args.d)


lines = file.readlines()
initNode, y_min, y_max= parse(lines)
lowerBound = []
upperBound = []
while initNode:
	for key in sorted(initNode.lowerBound):
		lowerBound.append(initNode.lowerBound[key])
	for key in sorted(initNode.upperBound):
		upperBound.append(initNode.upperBound[key])
	if len(initNode.child)>0:
		initNode = initNode.child.popitem()[1]
	else:
		initNode = None

rrtPlot(lowerBound, upperBound, dim[0], dim[1], goal, unsafes, regions )



