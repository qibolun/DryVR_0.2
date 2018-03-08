import sys

from src.core.dryvrmain import verify
from src.common.io import parseVerificationInputFile
from src.common.utils import importSimFunction

assert ".json" in sys.argv[-1], "Please provide json input file"

params = parseVerificationInputFile(sys.argv[-1])
simFunction = importSimFunction(params.path)

verify(params, simFunction)