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
    
    """
    @brief Converts geodetic coordinates (latitude, longitude, altitude) to ECEF coordinates.
    @param lat (float): Geodetic latitude in degrees.
    @param lon (float): Geodetic longitude in degrees.
    @param alt (float): Altitude above the ellipsoid in meters.
    @return ecef_x (float): ECEF x-coordinate in meters.
    @return ecef_y (float): ECEF y-coordinate in meters.
    @return ecef_z (float): ECEF z-coordinate in meters.
    """

    # WGS84 constants
    a = 6378137.0  # semi-major axis in meters
    f = 1 / 298.257223563  # flattening
    e = 0.081819190842622

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    cos_lat = math.cos(lat_rad)
    sin_lat = math.sin(lat_rad)
    N = a / math.sqrt(1 - f * (2 - f) * sin_lat**2)

    # calculate ECEF coordinates
    ecef_x = (N + alt) * cos_lat * math.cos(lon_rad)
    ecef_y = (N + alt) * cos_lat * math.sin(lon_rad)
    ecef_z = ((1-(e**2)) * N + alt) * sin_lat

    return ecef_x, ecef_y, ecef_z

  def ecef2lla(x, y, z):
    
    """
    @brief Converts ECEF coordinates to geodetic coordinates (latitude, longitude, altitude).
    @param x (float): ECEF x-coordinate in meters.
    @param y (float): ECEF y-coordinate in meters.
    @param z (float): ECEF z-coordinate in meters.
    @return lat (float): Geodetic latitude in degrees.
    @return lon (float): Geodetic longitude in degrees.
    @return alt (float): Altitude above the ellipsoid in meters.
    """
    
    # WGS84 ellipsoid constants:
    a = 6378137
    e = 8.1819190842622e-2
    
    b = math.sqrt(a**2 * (1 - e**2))
    ep = math.sqrt((a**2 - b**2) / b**2)
    p = math.sqrt(x**2 + y**2)
    th = math.atan2(a * z, b * p)
    lon = math.atan2(y, x)
    lat = math.atan2((z + ep**2 * b * math.sin(th)**3), (p - e**2 * a * math.cos(th)**3))
    N = a / math.sqrt(1 - e**2 * math.sin(lat)**2)
    alt = p / math.cos(lat) - N
    
    # return lon in range [0, 2*pi)
    lon = lon % (2 * math.pi)
    
    # correct for numerical instability in altitude near exact poles:
    k = abs(x) < 1e-10 and abs(y) < 1e-10
    alt = abs(z) - b if k else alt

    lat = math.degrees(lat)
    lon = math.degrees(lon)
    
    return lat, lon, alt

  def enu2ecef(e1, n1, u1, lat, lon, alt):
    
    """
    @brief Converts East-North-Up (ENU) coordinates to ECEF coordinates.
    @param e1 (float): Target east ENU coordinate in meters.
    @param n1 (float): Target north ENU coordinate in meters.
    @param u1 (float): Target up ENU coordinate in meters.
    @param lat (float): Observer geodetic latitude in degrees.
    @param lon (float): Observer geodetic longitude in degrees.
    @param alt (float): Observer geodetic altitude in meters.
    @return x (float): Target x ECEF coordinate in meters.
    @return y (float): Target y ECEF coordinate in meters.
    @return z (float): Target z ECEF coordinate in meters.
    """
    
    x0, y0, z0 = Geometry.lla2ecef(lat, lon, alt)
    dx, dy, dz = Geometry.enu2uvw(e1, n1, u1, lat, lon)

    return x0 + dx, y0 + dy, z0 + dz

  def enu2uvw(east, north, up, lat, lon):
    
    """
    @brief Converts East-North-Up (ENU) coordinates to UVW coordinates.
    @param east (float): Target east ENU coordinate in meters.
    @param north (float): Target north ENU coordinate in meters.
    @param up (float): Target up ENU coordinate in meters.
    @param lat (float): Observer geodetic latitude in degrees.
    @param lon (float): Observer geodetic longitude in degrees.
    @return u (float): Target u coordinate in meters.
    @return v (float): Target v coordinate in meters.
    @return w (float): Target w coordinate in meters.
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
    @brief Converts ECEF coordinates to East-North-Up (ENU) coordinates.
    @param x (float): Target x ECEF coordinate in meters.
    @param y (float): Target y ECEF coordinate in meters.
    @param z (float): Target z ECEF coordinate in meters.
    @param lat (float): Observer geodetic latitude in degrees.
    @param lon (float): Observer geodetic longitude in degrees.
    @param alt (float): Observer geodetic altitude in meters.
    @return east (float): Target east ENU coordinate in meters.
    @return north (float): Target north ENU coordinate in meters.
    @return up (float): Target up ENU coordinate in meters.
    """

    x0, y0, z0 = Geometry.lla2ecef(lat, lon, alt)
    return Geometry.uvw2enu(x - x0, y - y0, z - z0, lat, lon)

  def uvw2enu(u, v, w, lat, lon):
    
    """
    @brief Converts UVW coordinates to East-North-Up (ENU) coordinates.
    @param u (float): Shifted ECEF coordinate in the u-direction (m).
    @param v (float): Shifted ECEF coordinate in the v-direction (m).
    @param w (float): Shifted ECEF coordinate in the w-direction (m).
    @param lat (float): Observer geodetic latitude in degrees.
    @param lon (float): Observer geodetic longitude in degrees.
    @return e (float): Target east ENU coordinate in meters.
    @return n (float): Target north ENU coordinate in meters.
    @return u (float): Target up ENU coordinate in meters.
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

  def distance_ecef(point1, point2):
    
    """
    @brief Computes the Euclidean distance between two points in ECEF coordinates.
    @param point1 (tuple): Coordinates of the first point (x, y, z) in meters.
    @param point2 (tuple): Coordinates of the second point (x, y, z) in meters.
    @return distance (float): Euclidean distance between the two points in meters.
    """
    
    return math.sqrt(
      (point2[0]-point1[0])**2 +
      (point2[1]-point1[1])**2 +
      (point2[2]-point1[2])**2)

  def average_points(points):
    
    """
    @brief Computes the average point from a list of points.
    @param points (list): List of points, where each point is a tuple of coordinates (x, y, z) in meters.
    @return average_point (list): Coordinates of the average point (x_avg, y_avg, z_avg) in meters.
    """
    
    return [sum(coord) / len(coord) for coord in zip(*points)]
