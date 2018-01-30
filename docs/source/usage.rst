Usage
===================

Run DryVR Verfication
^^^^^^^^^^^^^^^^^^^^^^

To run DryVR verfication, please run: ::

	python main.py input/*/[input_file]

for example: ::

	python main.py input/daginput/input_thermo.json


Run DryVR Control Synthesis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run DryVR graph search algorithm, please run: ::

	python rrt.py input/*/[input_file]

for example: ::

	python rrt.py input/rrtinput/mazefinder.json


Plotter
^^^^^^^^^^^^^^^

After you run the our tool, a reachtube.txt file will be generated in output folder unless the model is determined unsafe during simulation test.

To plot the reachtube, please run: ::

	python plotter.py -x [x dimension number] -y [y dimension number list] -f [input file name] -o [output file name]

-x is the dimension number for x-axis, the default value will be 0, which is the dimension of time. 

-y is dimension number lists indicates the dimension you want to draw for y-axis. For example -y [1,2]. The default value will be [1].

-f is the file path for reach tube file that you want to plot, the default value will be output/reachtube.txt. 

-o is output file option, the default value is plotResult.png.  

To get help for plotter, please run: ::

	python plotter.py -h

Note that the dimension 0 is local time and last dimension is global time. For example, input_AEB's inital set is [[0.0,-23.0,0.0,1.0,0.0,-15.0,0.0,1.0],[0.0,-22.8,0.0,1.0,0.0,-15.0,0.0,1.0]]. Therefore, it has 8 dimensions in total. You can choose to plot dimension from 0 to 9. Where dimension 0 is the local time and dimension 9 is global time. Dimension 1~8 is corresponding to the dimension you specify in initial set.

for example: ::

	python plotter.py -y [1,2] -f output/reachtube.txt 


More plot results can be found at the :ref:`example-label` page.
