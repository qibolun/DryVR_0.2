"""
This file contains reach tube class for DryVR
"""

class ReachTube():
	"""
    This is class is an object for reach tube
    Ideally it should support to fetch reachtube by mode and variable name
    And it should allow users to plot the reach tube in different ways
    """
	def __init__(self, tube, modes):
		"""
        ReachTube class initialization function.

        Args:
        	tube (list): raw reach tube (that used to print to file)
            variables (list): list of variables in the reach tube
            modes (list): list of modes in the reach ReachTube
        """