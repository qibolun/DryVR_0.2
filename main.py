import json
import sys

from src.core.dryvrmain import verify
from src.common.utils import importSimFunction

from src.plotter.parser import parse


assert ".json" in sys.argv[-1], "Please provide json input file"
with open(sys.argv[-1], 'r') as f:
	data = json.load(f)
	simFunction = importSimFunction(data["directory"])
	safey, reach = verify(data, simFunction)
	lines = reach.raw.split("\n")
	print type(lines[0]), lines[0]
	initNode, y_min, y_max= parse(lines)
