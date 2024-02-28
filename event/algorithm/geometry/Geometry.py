"""
@file Geometry.py
@author 30hours
"""

import math
import numpy as np
import pyproj

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
        e = 0.081819190842622

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
        #ecef_z = (N * (1 - f) + altitude) * sin_lat
        ecef_z = ((1-(e**2)) * N + altitude) * sin_lat

        return ecef_x, ecef_y, ecef_z

    # def ecef2lla(x, y, z):
      
    #     # WGS84 parameters
    #     a = 6378137.0  # semi-major axis in meters
    #     f = 1 / 298.257223563  # flattening
    #     b = (1 - f) * a  # semi-minor axis

    #     # Calculate eccentricity squared
    #     e_squared = (a**2 - b**2) / a**2

    #     # Calculate longitude
    #     lon = math.atan2(y, x)

    #     # Calculate distance from the origin to the XY plane
    #     r = math.sqrt(x**2 + y**2)

    #     # Calculate latitude
    #     lat = math.atan2(z, r)

    #     # Calculate altitude
    #     sin_lat = math.sin(lat)
    #     N = a / math.sqrt(1 - e_squared * sin_lat**2)
    #     alt = r / math.cos(lat) - N

    #     return math.degrees(lat), math.degrees(lon), alt

    # def ecef2lla(x, y, z):

    #     # WGS84 ellipsoid constants
    #     a = 6378137
    #     es = (8.1819190842622e-2) ** 2

    #     # Calculations
    #     b = np.sqrt(a ** 2 * (1 - es))
    #     ep = (a ** 2 - b ** 2) / b ** 2

    #     p = np.sqrt(x ** 2 + y ** 2)
    #     th = np.arctan2(a * z, b * p)
    #     lon = np.arctan2(y, x)
    #     lat = np.arctan2(z + ep ** 2 * b * np.sin(th) ** 3, p - es ** 2 * a * np.cos(th) ** 3)
    #     N = a / np.sqrt(1 - es * np.sin(lat) ** 2)
    #     alt = p / np.cos(lat) - N

    #     # Return lon in range [0, 2*pi)
    #     lon = np.mod(lon, 2 * np.pi)

    #     # Correct for numerical instability in altitude near exact poles
    #     # (after this correction, error is about 2 millimeters, which is about
    #     # the same as the numerical precision of the overall function)
    #     k = np.abs(x) < 1e-3  # Use x for the condition
    #     alt = np.where(k, np.abs(z) - b, alt)

    #     # Convert radians to degrees
    #     lat = lat * (180 / np.pi)
    #     lon = lon * (180 / np.pi)
    
    #     return lat, lon, alt

    def ecef2lla(x, y, z):
        # WGS84 ellipsoid constants:
        a = 6378137
        e = 8.1819190842622e-2
        
        # Calculations:
        b = np.sqrt(a**2 * (1 - e**2))
        ep = np.sqrt((a**2 - b**2) / b**2)
        p = np.sqrt(x**2 + y**2)
        th = np.arctan2(a * z, b * p)
        lon = np.arctan2(y, x)
        lat = np.arctan2((z + ep**2 * b * np.sin(th)**3), (p - e**2 * a * np.cos(th)**3))
        N = a / np.sqrt(1 - e**2 * np.sin(lat)**2)
        alt = p / np.cos(lat) - N
        
        # Return lon in range [0, 2*pi)
        lon = np.mod(lon, 2 * np.pi)
        
        # Correct for numerical instability in altitude near exact poles:
        # (after this correction, error is about 2 millimeters, which is about
        # the same as the numerical precision of the overall function)
        k = np.logical_and(np.abs(x) < 1e-10, np.abs(y) < 1e-10)
        alt = np.where(k, np.abs(z) - b, alt)

        lat = np.degrees(lat)
        lon = np.degrees(lon)
        
        return lat, lon, alt