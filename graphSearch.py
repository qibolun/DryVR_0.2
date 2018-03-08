import sys

from src.core.dryvrmain import graphSearch
from src.common.io import parseRrtInputFile
from src.common.utils import importSimFunction

assert ".json" in sys.argv[-1], "Please provide json input file"


params = parseRrtInputFile(sys.argv[-1])
simFunction = importSimFunction(params.path)

graphSearch(params, simFunction)