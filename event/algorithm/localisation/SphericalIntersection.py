"""
@file SphericalIntersection.py
@author 30hours
"""

from data.Ellipsoid import Ellipsoid
from algorithm.geometry.Geometry import Geometry
import numpy as np
import math

class SphericalIntersection:

    """
    @class SphericalIntersection
    @brief A class for intersecting ellipsoids using SX method.
    @details Uses associated detections from multiple radars.
    @see blah2 at https://github.com/30hours/blah2.
    """

    def __init__(self):

        """
        @brief Constructor for the SphericalIntersection class.
        """

    def process(self, assoc_detections, radar_data):

        """
        @brief Perform target localisation using the SX method.
        @param assoc_detections (dict): JSON of blah2 radar detections.
        @param radar_data (dict): JSON of adsb2dd truth detections.
        @return dict: Dict of associated detections.
        """

        output = {}

        return output