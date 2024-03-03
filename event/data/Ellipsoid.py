"""
@file Ellipsoid.py
@author 30hours
"""

import math
from algorithm.geometry.Geometry import Geometry

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
        self.midpoint_lla = Geometry.ecef2lla(
          self.midpoint[0], self.midpoint[1], self.midpoint[2])
        vector_enu = Geometry.ecef2enu(f1[0], f1[1], f1[2], 
          self.midpoint_lla[0], self.midpoint_lla[1], self.midpoint_lla[2])
        self.yaw = -math.atan2(vector_enu[1], vector_enu[0])
        self.pitch = math.atan2(vector_enu[2], 
          math.sqrt(vector_enu[0]**2 + vector_enu[1]**2))
        self.distance = math.sqrt(
        (f2[0] - f1[0])**2 +
        (f2[1] - f1[1])**2 +
        (f2[2] - f1[2])**2)
