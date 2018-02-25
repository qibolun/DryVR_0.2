"""
This file contains initial set class for DryVR
"""

class InitialSet():
    """
    This is class to represent the initial set
    """
    def __init__(self, lower, upper):
        """
        Initial set class initialization function.

        Args:
            lower (list): lowerbound of the initial set
            upper (list): upperbound of the initial set
        """

        self.lowerBound = lower
        self.upperBound = upper
        self.delta = [(upper[i]-lower[i])/2.0 for i in range(len(upper))]
        # Child point points to children InitialSetStack obj
        # This it how it works
        # Since a initial set can generate a reach tube that intersect
        # with different guards
        # So there can be multiple children pointers
        # Therefore this is a dictionary obj
        # self.child["MODEA"] = InitialSetStack for MODEA
        self.child = {}
        self.bloatedTube = []
    
    def refine(self):
        """
        This function refine the current initial set into two smaller set

        Args:
            None
        Returns:
            two refined initial set

        """
        # Refine the initial set into two smaller set
        # based on index with largest delta
        idx = self.delta.index(max(self.delta))
        # Construct first smaller initial set
        initSetOneUB = list(self.upperBound)
        initSetOneLB = list(self.lowerBound)
        initSetOneLB[idx] += self.delta[idx]
        # Construct second smaller initial set
        initSetTwoUB = list(self.upperBound)
        initSetTwoLB = list(self.lowerBound)
        initSetTwoUB[idx] -= self.delta[idx]

        return (
            InitialSet(initSetOneLB, initSetOneUB),
            InitialSet(initSetTwoLB, initSetTwoUB),
        )

    def __str__(self):
        """
        Build string representation for the initial set

        Args:
            None
        Returns:
            A string describes the initial set

        """
        ret = ""
        ret += "Lower Bound: "+str(self.lowerBound)+"\n"
        ret += "Upper Bound: "+str(self.upperBound)+"\n"
        ret += "Delta: "+str(self.delta)+"\n"
        return ret 
