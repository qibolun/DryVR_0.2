DryVR 2.0 is a software for hybrid system verification. Please find the documentation at 

http://dryvr-02.readthedocs.io/en/latest/

Installation
==================
To install the required packages, please run:
-------------------------------------------------------------
sudo ./installRequirement.sh

The current version of installation file has been tested on a clean install of Ubuntu 16.04. 

Quick Start
==================
To run verification examples, please run 
-------------------------------------------------------------
python main.py input/[input_file]

for example:

python main.py input/daginput/input_thermo.json

The examples descriptions can be found in the documentation. Please note that as the verification algorithm uses probabilistic method, the verification result may vary for different runs.


To run controller synthesis, please run:
------------------------------------------------------------
python graphSearch.py input/[input_file]

for example:

python graphSearch.py input/rrtinput/mazefinder.json

