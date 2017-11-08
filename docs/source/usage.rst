Usage
===================

Run DryVR
^^^^^^^^^^^^^^^

To run DryVR, please run: ::

	python main.py input/*/[input_file]

for example: ::

	python main.py input/daginput/input_thermo.json


Plotter
^^^^^^^^^^^^^^^

After you run the our tool, a reachtube.txt file will be generated in output folder unless the model is determined unsafe during simulation test.

To plot the reachtube, please run: ::

	python plotter.py -d [dimension Number] -f [file name]

Where dimension number indicates the dimension you want to draw.It should be an array, For example -d [1,2]. The default value will be [1], for the file option,
The default value will be -f output/reachtube.txt. Note that the dimension 0 is local time and last dimension is global time. For example, input_AEB's inital set is [[0.0,-23.0,0.0,1.0,0.0,-15.0,0.0,1.0],[0.0,-22.8,0.0,1.0,0.0,-15.0,0.0,1.0]]. Therefore, it has 8 dimensions in total. You can choose to plot dimension from 0 to 9. Where dimension 0 is the local time and dimension 9 is global time. Dimension 1~8 is corresponding to the dimension you specify in initial set.

for example: ::

	python plotter.py -d [1,2] -f output/reachtube.txt 





More plot results can be found at the :ref:`example-label` page.
