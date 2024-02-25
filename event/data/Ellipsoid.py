"""
@file Ellipsoid.py
@author 30hours
"""

import math

class Ellipsoid:

    """
    @class Ellipsoid
    @brief A class to store ellipsoid parameters for bistatic radar.
    @details Stores foci, midpoint, pitch, yaw and distance.
    """

    def __init__(self, f1, f2, name):

        """
        @brief Constructor for the Ellipsoid class.
        @param f1 (list): [x, y, z] of foci 1 in ECEF.
        @param f2 (list): [x, y, z] of foci 2 in ECEF.
        @param name (str): Name to associate with shape.
        """

        self.f1 = f1
        self.f2 = f2
        self.name = name

        # dependent members
        self.midpoint = [(f1[0]+f2[0])/2, 
          (f1[1]+f2[1])/2, (f1[2]+f2[2])/2]
        vector = (f2[0]-f1[0], f2[1]-f1[1], f2[2]-f1[2])
        self.yaw = math.atan2(vector[1], vector[0])
        self.pitch = math.atan2(vector[2], 
          math.sqrt(vector[0]**2 + vector[1]**2))
        self.distance = math.sqrt(
        (f2[0] - f1[0])**2 +
        (f2[1] - f1[1])**2 +
        (f2[2] - f1[2])**2)
