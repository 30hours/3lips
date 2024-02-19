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
    Able to generate samples through public functions.
    """

    def __init__(self, f1, f2, name):

        """
        @brief Constructor for the Ellipsoid class.
        """

        self.f1 = f1
        self.f2 = f2
        self.name = name

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

    def process(self, bistatic_range):

        """
        @brief Perform coord registration using the ellipsoid parametric method.
        @details Generate a (non arc-length) parametric ellipsoid for each node.
        Find 
        @param radar_detections (str): JSON of blah2 radar detections.
        @param adsb_detections (str): JSON of adsb2dd truth detections.
        @return str: JSON of associated detections.
        """

        output = {}

        return output
        