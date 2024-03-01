"""
@file Geometry.py
@author 30hours
"""

import math

class Geometry:

    """
    @class Geometry
    @brief A class to store geometric functions.
    @details Assumes WGS-84 ellipsoid for all functions.
    """

    def __init__(self):

        """
        @brief Constructor for the Geometry class.
        """

    def lla2ecef(lat, lon, alt):

        # WGS84 constants
        a = 6378137.0  # semi-major axis in meters
        f = 1 / 298.257223563  # flattening
        e = 0.081819190842622

        # Convert latitude and longitude to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)

        # Calculate the auxiliary values
        cos_lat = math.cos(lat_rad)
        sin_lat = math.sin(lat_rad)
        N = a / math.sqrt(1 - f * (2 - f) * sin_lat**2)

        # Calculate ECEF coordinates
        ecef_x = (N + alt) * cos_lat * math.cos(lon_rad)
        ecef_y = (N + alt) * cos_lat * math.sin(lon_rad)
        ecef_z = ((1-(e**2)) * N + alt) * sin_lat

        return ecef_x, ecef_y, ecef_z

    def ecef2lla(x, y, z):
        # WGS84 ellipsoid constants:
        a = 6378137
        e = 8.1819190842622e-2
        
        # Calculations:
        b = math.sqrt(a**2 * (1 - e**2))
        ep = math.sqrt((a**2 - b**2) / b**2)
        p = math.sqrt(x**2 + y**2)
        th = math.atan2(a * z, b * p)
        lon = math.atan2(y, x)
        lat = math.atan2((z + ep**2 * b * math.sin(th)**3), (p - e**2 * a * math.cos(th)**3))
        N = a / math.sqrt(1 - e**2 * math.sin(lat)**2)
        alt = p / math.cos(lat) - N
        
        # Return lon in range [0, 2*pi)
        lon = lon % (2 * math.pi)
        
        # Correct for numerical instability in altitude near exact poles:
        # (after this correction, error is about 2 millimeters, which is about
        # the same as the numerical precision of the overall function)
        k = abs(x) < 1e-10 and abs(y) < 1e-10
        alt = abs(z) - b if k else alt

        lat = math.degrees(lat)
        lon = math.degrees(lon)
        
        return lat, lon, alt

    def enu2ecef(e1, n1, u1, lat, lon, alt):
        """
        ENU to ECEF

        Parameters
        ----------

        e1 : float
            target east ENU coordinate (meters)
        n1 : float
            target north ENU coordinate (meters)
        u1 : float
            target up ENU coordinate (meters)
        lat0 : float
              Observer geodetic latitude
        lon0 : float
              Observer geodetic longitude
        h0 : float
            observer altitude above geodetic ellipsoid (meters)


        Results
        -------
        x : float
            target x ECEF coordinate (meters)
        y : float
            target y ECEF coordinate (meters)
        z : float
            target z ECEF coordinate (meters)
        """
        x0, y0, z0 = Geometry.lla2ecef(lat, lon, alt)
        dx, dy, dz = Geometry.enu2uvw(e1, n1, u1, lat, lon)

        return x0 + dx, y0 + dy, z0 + dz

    def enu2uvw(east, north, up, lat, lon):
        """
        Parameters
        ----------

        e1 : float
            target east ENU coordinate (meters)
        n1 : float
            target north ENU coordinate (meters)
        u1 : float
            target up ENU coordinate (meters)

        Results
        -------

        u : float
        v : float
        w : float
        """

        lat = math.radians(lat)
        lon = math.radians(lon)

        t = math.cos(lat) * up - math.sin(lat) * north
        w = math.sin(lat) * up + math.cos(lat) * north

        u = math.cos(lon) * t - math.sin(lon) * east
        v = math.sin(lon) * t + math.cos(lon) * east

        return u, v, w

    def ecef2enu(x, y, z, lat, lon, alt):

        """
        @brief From observer to target, ECEF => ENU.
        @param x (float): Target x ECEF coordinate (m).
        @param y (float): Target y ECEF coordinate (m).
        @param z (float): Target z ECEF coordinate (m).
        @param lat (float): Observer geodetic latitude (deg).
        @param lon (float): Observer geodetic longitude (deg).
        @param alt (float): Observer geodetic altituder (m).
        @return east (float): Target east ENU coordinate (m).
        @return north (float): Target north ENU coordinate (m).
        @return up (float): Target up ENU coordinate (m).
        """

        x0, y0, z0 = Geometry.lla2ecef(lat, lon, alt)
        return Geometry.uvw2enu(x - x0, y - y0, z - z0, lat, lon)

    def uvw2enu(u, v, w, lat, lon):

        """
        @brief 
        @param u (float): Shifted ECEF coordinate (m).
        @param v (float): Shifted ECEF coordinate (m).
        @param w (float): Shifted ECEF coordinate (m).
        @param lat (float): Observer geodetic latitude (deg).
        @param lon (float): Observer geodetic longitude (deg).
        @param e (float): Target east ENU coordinate (m).
        @param n (float): Target north ENU coordinate (m).
        @param u (float): Target up ENU coordinate (m).
        """

        lat = math.radians(lat)
        lon = math.radians(lon)

        cos_lat = math.cos(lat)
        sin_lat = math.sin(lat)
        cos_lon = math.cos(lon)
        sin_lon = math.sin(lon)

        t = cos_lon * u + sin_lon * v
        e = -sin_lon * u + cos_lon * v
        u = cos_lat * t + sin_lat * w
        n = -sin_lat * t + cos_lat * w

        return e, n, u