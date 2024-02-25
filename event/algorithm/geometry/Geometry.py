"""
@file Geometry.py
@author 30hours
"""

import math
import numpy as np

class Geometry:

    """
    @class Geometry
    @brief A class to store geometric functions.
    """

    def __init__(self, f1, f2, name):

        """
        @brief Constructor for the Ellipsoid class.
        """

    def lla2ecef(latitude, longitude, altitude):

        # WGS84 constants
        a = 6378137.0  # semi-major axis in meters
        f = 1 / 298.257223563  # flattening

        # Convert latitude and longitude to radians
        lat_rad = math.radians(latitude)
        lon_rad = math.radians(longitude)

        # Calculate the auxiliary values
        cos_lat = math.cos(lat_rad)
        sin_lat = math.sin(lat_rad)
        N = a / math.sqrt(1 - f * (2 - f) * sin_lat**2)

        # Calculate ECEF coordinates
        ecef_x = (N + altitude) * cos_lat * math.cos(lon_rad)
        ecef_y = (N + altitude) * cos_lat * math.sin(lon_rad)
        ecef_z = (N * (1 - f) + altitude) * sin_lat

        return ecef_x, ecef_y, ecef_z
