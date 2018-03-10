import json
import sys

from src.core.dryvrmain import verify
from src.common.utils import importSimFunction

assert ".json" in sys.argv[-1], "Please provide json input file"
with open(sys.argv[-1], 'r') as f:
	data = json.load(f)
	simFunction = importSimFunction(data["directory"])
	verify(data, simFunction)