import argparse

from src.plotter.parser import parse

parser = argparse.ArgumentParser(
	description = 'This is plotter script for DryVR generated reach tube output'
)

parser.add_argument('-f', type=str, default='output/reachtube.txt', help='file path for reach tube')
parser.add_argument('-d', type=int, default='1', help='dimension number you want to plot')
args = parser.parse_args()

try:
	file = open(args.f, 'r')
except IOError:
	print ('File does not exist')

lines = file.readlines()
initNode = parse(lines)
