"""
@file EllipsoidParametric.py
@author 30hours
"""

from data.Ellipsoid import Ellipsoid
from algorithm.geometry.Geometry import Geometry
import numpy as np

class EllipsoidParametric:

    """
    @class EllipsoidParametric
    @brief A class for intersecting ellipsoids using a parametric approx.
    @details Uses associated detections from multiple radars.
    @see blah2 at https://github.com/30hours/blah2.
    """

    def __init__(self):

        """
        @brief Constructor for the EllipsoidParametric class.
        """

        self.ellipsoids = []

    def process(self, assoc_detections, radar_data):

        """
        @brief Perform coord registration using the ellipsoid parametric method.
        @details Generate a (non arc-length) parametric ellipsoid for each node.
        @param assoc_detections (dict): JSON of blah2 radar detections.
        @param radar_data (dict): JSON of adsb2dd truth detections.
        @return str: JSON of associated detections.
        """

        output = {}

        # return if no detections
        if not assoc_detections:
          return output

        for target in assoc_detections:

            print(target, flush=True)

            for radar in assoc_detections[target]:

                print(radar["radar"], flush=True)
                print(radar["delay"], flush=True)

                # create ellipsoid for radar
                ellipsoid = next((
                  item for item in self.ellipsoids 
                  if item.name == radar["radar"]), None)

                if ellipsoid is None:
                  config = radar_data[radar["radar"]]["config"]
                  x_tx, y_tx, z_tx = Geometry.lla2ecef(
                    config['location']['tx']['latitude'],
                    config['location']['tx']['longitude'],
                    config['location']['tx']['altitude']
                  )
                  x_rx, y_rx, z_rx = Geometry.lla2ecef(
                    config['location']['rx']['latitude'],
                    config['location']['rx']['longitude'],
                    config['location']['rx']['altitude']
                  )
                  ellipsoid = Ellipsoid(
                    [x_tx, y_tx, z_tx],
                    [x_rx, y_rx, z_rx],
                    radar["radar"]
                  )

                print(ellipsoid.yaw, flush=True)
                print(ellipsoid.pitch, flush=True)

                self.sample(ellipsoid, radar["delay"], 10000)

            print("", flush=True)

        return output

    def sample(self, ellipsoid, bistatic_range, n):

        """
        @brief Generate a set of points for the ellipsoid.
        @details No arc length parametrisation.
        @param ellipsoid (Ellipsoid): The ellipsoid object to use.
        @param bistatic_range (float): Bistatic range for ellipsoid.
        @param n (int): Number of points to generate.
        @return list: Samples with size [n, 3].
        """

        # rotation matrix
        phi = ellipsoid.pitch
        theta = ellipsoid.yaw
        R = np.array([
          [np.cos(phi)*np.cos(theta), -np.sin(phi)*np.cos(theta), np.sin(theta)],
          [np.sin(phi), np.cos(phi), 0],
          [-np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)]
        ])

        # compute samples vectorised
        a = (bistatic_range-ellipsoid.distance)/2
        b = np.sqrt(a**2 - (ellipsoid.distance/2))
        u_values = np.linspace(0, 2 * np.pi, n)
        v_values = np.linspace(-np.pi/2, np.pi/2, n)
        u, v = np.meshgrid(u_values, v_values, indexing='ij')
        x = a * np.cos(u)
        y = b * np.sin(u) * np.cos(v)
        z = b * np.sin(u) * np.sin(v)
        r = np.stack([x, y, z], axis=-1).reshape(-1, 3)

        r_1 = np.dot(r, R) + ellipsoid.midpoint

        return r_1.tolist()