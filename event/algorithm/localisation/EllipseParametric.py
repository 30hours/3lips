"""
@file EllipseParametric.py
@author 30hours
"""

from data.Ellipsoid import Ellipsoid
from algorithm.geometry.Geometry import Geometry
import numpy as np
import math

class EllipseParametric:

    """
    @class EllipseParametric
    @brief A class for intersecting ellipses using a parametric approx.
    @details Uses associated detections from multiple radars.
    @see blah2 at https://github.com/30hours/blah2.
    """

    def __init__(self):

        """
        @brief Constructor for the EllipseParametric class.
        """

        self.ellipsoids = []
        self.nSamples = 150
        self.threshold  = 800

    def process(self, assoc_detections, radar_data):

        """
        @brief Perform target localisation using the ellipse parametric method.
        @details Generate a (non arc-length) parametric ellipse for each node.
        @param assoc_detections (dict): JSON of blah2 radar detections.
        @param radar_data (dict): JSON of adsb2dd truth detections.
        @return dict: Dict of associated detections.
        """

        output = {}

        # return if no detections
        if not assoc_detections:
          return output

        for target in assoc_detections:

            print(target, flush=True)
            target_samples = {}
            target_samples[target] = {}

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

                samples = self.sample(ellipsoid, radar["delay"]*1000, self.nSamples)
                target_samples[target][radar["radar"]] = samples

            # find close points, ellipse 1 is master
            radar_keys = list(target_samples[target].keys())
            samples_intersect = []

            # loop points in master ellipsoid
            for point1 in target_samples[target][radar_keys[0]]:
                valid_point = True
                # loop over each other list
                for i in range(1, len(radar_keys)):
                    # loop points in other list
                    if not any(Geometry.distance_ecef(point1, point2) < self.threshold 
                      for point2 in target_samples[target][radar_keys[i]]):
                        valid_point = False
                        break
                if valid_point:
                    samples_intersect.append(point1)

            # remove duplicates and convert to LLA
            output[target] = {}
            output[target]["points"] = []
            for i in range(len(samples_intersect)):
              samples_intersect[i] = Geometry.ecef2lla(
                samples_intersect[i][0], 
                samples_intersect[i][1], 
                0)
              output[target]["points"].append([
                round(samples_intersect[i][0], 3),
                round(samples_intersect[i][1], 3),
                0])

        return output

    def sample(self, ellipsoid, bistatic_range, n):

        """
        @brief Generate a set of ECEF points for the ellipse.
        @details No arc length parametrisation.
        @details Use ECEF because distance measure is simple over LLA.
        @param ellipsoid (Ellipsoid): The ellipsoid object to use.
        @param bistatic_range (float): Bistatic range for ellipse.
        @param n (int): Number of points to generate.
        @return list: Samples with size [n, 3].
        """

        # rotation matrix
        theta = ellipsoid.yaw
        R = np.array([
          [np.cos(theta), -np.sin(theta)],
          [np.sin(theta), np.cos(theta)]
        ])

        # compute samples vectorised
        a = (bistatic_range+ellipsoid.distance)/2
        b = np.sqrt(a**2 - (ellipsoid.distance/2)**2)
        u = np.linspace(0, 2 * np.pi, n)
        x = a * np.cos(u)
        y = b * np.sin(u)
        r = np.stack([x, y], axis=-1).reshape(-1, 2)

        r_1 = np.dot(r, R)
        output = []

        for i in range(len(r_1)):
          # points to ECEF
          x, y, z = Geometry.enu2ecef(
            r_1[i][0], r_1[i][1], 0, 
            ellipsoid.midpoint_lla[0], 
            ellipsoid.midpoint_lla[1], 
            ellipsoid.midpoint_lla[2])
          # points to LLA
          [x, y, z] = Geometry.ecef2lla(x, y, z)
          # only store points above ground
          if z > 0:
            # convert back to ECEF for simple distance measurements
            [x, y, z] = Geometry.lla2ecef(x, y, z)
            output.append([round(x, 3), round(y, 3), 0])

        return output