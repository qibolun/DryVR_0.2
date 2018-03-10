import json
import sys

from src.core.dryvrmain import graphSearch
from src.common.io import parseRrtInputFile
from src.common.utils import importSimFunction

assert ".json" in sys.argv[-1], "Please provide json input file"
with open(sys.argv[-1], 'r') as f:
	data = json.load(f)
	simFunction = importSimFunction(data["directory"])
	graphSearch(data, simFunction)