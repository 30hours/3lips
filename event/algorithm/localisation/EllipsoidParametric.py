"""
@file EllipsoidParametric.py
@author 30hours
"""

from data.Ellipsoid import Ellipsoid
from algorithm.geometry.Geometry import Geometry
import numpy as np
import math

class EllipsoidParametric:

    """
    @class EllipsoidParametric
    @brief A class for intersecting ellipsoids using a parametric approx.
    @details Uses associated detections from multiple radars.
    @see blah2 at https://github.com/30hours/blah2.
    """

    def __init__(self, method="mean", nSamples=100, threshold=500):

        """
        @brief Constructor for the EllipsoidParametric class.
        """

        self.ellipsoids = []
        self.nSamples = nSamples
        self.threshold  = threshold
        self.method = method

    def process(self, assoc_detections, radar_data):

        """
        @brief Perform target localisation using the ellipsoid parametric method.
        @details Generate a (non arc-length) parametric ellipsoid for each node.
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

            # find close points, ellipsoid 1 is master
            radar_keys = list(target_samples[target].keys())
            samples_intersect = []

            if self.method == "mean":

                # loop points in main ellipsoid
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

                average_point = Geometry.average_points(samples_intersect)
                samples_intersect = [average_point]

                if len(samples_intersect) == 0:
                    return output 

            elif self.method == "minimum":

                min_distance = self.threshold
                min_point1 = None
                # loop points in main ellipsoid
                for point1 in target_samples[target][radar_keys[0]]:
                    valid_point = True
                    distance_from_point1 = [self.threshold]*(len(radar_keys)-1)
                    # loop over each other list
                    for i in range(1, len(radar_keys)):
                        if i > 1 and distance_from_point1[i-1] > self.threshold:
                            valid_point = False
                            break
                        # loop points in other list
                        for point2 in target_samples[target][radar_keys[i]]:
                            distance = Geometry.distance_ecef(point1, point2)
                            if distance < distance_from_point1[i-1]:
                                distance_from_point1[i-1] = distance
                    norm = math.sqrt(sum(x ** 2 for x in distance_from_point1))
                    if valid_point and norm < min_distance:
                        min_distance = norm
                        min_point1 = point1
                        
                if min_point1 is not None:        
                    samples_intersect.append(min_point1)
                else:
                    return output

            else:
                print('Invalid method.')
                return output

            # remove duplicates and convert to LLA
            output[target] = {}
            output[target]["points"] = []
            for i in range(len(samples_intersect)):
              samples_intersect[i] = Geometry.ecef2lla(
                samples_intersect[i][0], 
                samples_intersect[i][1], 
                samples_intersect[i][2])
              output[target]["points"].append([
                round(samples_intersect[i][0], 3),
                round(samples_intersect[i][1], 3),
                round(samples_intersect[i][2])])

        return output

    def sample(self, ellipsoid, bistatic_range, n):

        """
        @brief Generate a set of ECEF points for the ellipsoid.
        @details No arc length parametrisation.
        @details Use ECEF because distance measure is simple over LLA.
        @param ellipsoid (Ellipsoid): The ellipsoid object to use.
        @param bistatic_range (float): Bistatic range for ellipsoid.
        @param n (int): Number of points to generate.
        @return list: Samples with size [n, 3].
        """

        # rotation matrix
        phi = ellipsoid.pitch
        theta = ellipsoid.yaw
        R = np.array([
          [np.cos(theta), -np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi)],
          [np.sin(theta), np.cos(theta)*np.cos(phi), -np.cos(theta)*np.sin(phi)],
          [0, np.sin(phi), np.cos(phi)]
        ])

        # compute samples vectorised
        a = (bistatic_range+ellipsoid.distance)/2
        b = np.sqrt(a**2 - (ellipsoid.distance/2)**2)
        u_values = np.linspace(0, 2 * np.pi, n)
        v_values = np.linspace(-np.pi/2, np.pi/2, int(n/2))
        u, v = np.meshgrid(u_values, v_values, indexing='ij')
        x = a * np.cos(u)
        y = b * np.sin(u) * np.cos(v)
        z = b * np.sin(u) * np.sin(v)
        r = np.stack([x, y, z], axis=-1).reshape(-1, 3)

        r_1 = np.dot(r, R)
        output = []

        for i in range(len(r_1)):
          # points to ECEF
          x, y, z = Geometry.enu2ecef(
            r_1[i][0], r_1[i][1], r_1[i][2], 
            ellipsoid.midpoint_lla[0], 
            ellipsoid.midpoint_lla[1], 
            ellipsoid.midpoint_lla[2])
          # points to LLA
          [x, y, z] = Geometry.ecef2lla(x, y, z)
          # only store points above ground
          if z > 0:
            # convert back to ECEF for simple distance measurements
            [x, y, z] = Geometry.lla2ecef(x, y, z)
            output.append([round(x, 3), round(y, 3), round(z)])

        return output
