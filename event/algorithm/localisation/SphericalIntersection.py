"""
@file SphericalIntersection.py
@author 30hours
"""

from algorithm.geometry.Geometry import Geometry
import numpy as np
import math

class SphericalIntersection:

    """
    @class SphericalIntersection
    @brief A class for intersecting ellipsoids using SX method.
    @details Uses associated detections from multiple radars.
    @see https://ieeexplore.ieee.org/document/6129656
    """

    def __init__(self):

        """
        @brief Constructor for the SphericalIntersection class.
        """

        self.type = "rx"
        self.not_type = "rx" if self.type == "tx" else "tx"

    def process(self, assoc_detections, radar_data):

        """
        @brief Perform target localisation using the SX method.
        @param assoc_detections (dict): JSON of blah2 radar detections.
        @param radar_data (dict): JSON of adsb2dd truth detections.
        @return dict: Dict of associated detections.
        """

        output = {}

        # return if no detections
        if not assoc_detections:
          return output

        # pick first radar rx node as ENU reference (arbitrary)
        radar = next(iter(radar_data))
        reference_lla = [
          radar_data[radar]["config"]["location"][self.not_type]["latitude"], 
          radar_data[radar]["config"]["location"][self.not_type]["longitude"],
          radar_data[radar]["config"]["location"][self.not_type]["altitude"]]
        reference_ecef = Geometry.lla2ecef(reference_lla[0],
          reference_lla[1], reference_lla[2])

        for target in assoc_detections:

            nDetections = len(assoc_detections[target])

            # matrix of positions of non-constant node
            S = np.zeros((nDetections, 3))

            # additional vector
            z_vec = np.zeros((nDetections, 1))

            # bistatic range vector r
            r = np.zeros((nDetections, 1))

            for index, radar in enumerate(assoc_detections[target]):

                # convert position to ENU and add to S
                config = radar_data[radar["radar"]]["config"]
                x, y, z = Geometry.lla2ecef(
                  config['location'][self.type]['latitude'],
                  config['location'][self.type]['longitude'],
                  config['location'][self.type]['altitude'])
                x_enu, y_enu, z_enu = Geometry.ecef2enu(x, y, z, 
                  reference_lla[0], 
                  reference_lla[1], 
                  reference_lla[2])
                S[index, :] = [x_enu, y_enu, z_enu]

                # add to z
                distance = Geometry.distance_ecef(
                  [x, y, z], [reference_ecef[0], 
                  reference_ecef[1], reference_ecef[2]])
                R_i = (radar["delay"]*1000) + distance
                z_vec[index, :] = (x_enu**2 + y_enu**2 + z_enu**2 - R_i**2)/2

                # add to r
                r[index, :] = R_i

            # now compute matrix math
            S_star = np.linalg.inv(S.T @ S) @ S.T
            a = S_star @ z_vec
            b = S_star @ r
            R_t = [0, 0]
            discriminant = 4*((a.T @ b)**2) - 4*((b.T @ b) - 1)*(a.T @ a)
            if discriminant >= 0:
                R_t[0] = (-2*(a.T @ b) - np.sqrt(discriminant))/(2*((b.T @ b)-1))
                R_t[1] = (-2*(a.T @ b) + np.sqrt(discriminant))/(2*((b.T @ b)-1))
            else:
                R_t[0] = np.real((-2*(a.T @ b) - np.sqrt(discriminant + 0j))/(2*((b.T @ b)-1)))
                R_t[1] = np.real((-2*(a.T @ b) + np.sqrt(discriminant + 0j))/(2*((b.T @ b)-1)))
            x_t = [0, 0]
            x_t[0] = S_star @ (z_vec + r*R_t[0])
            x_t[1] = S_star @ (z_vec + r*R_t[1])

            # use solution with highest altitude
            output[target] = {}
            output[target]["points"] = []
            x_t_list = [np.squeeze(arr).tolist() for arr in x_t]

            # convert points back to LLA
            for index in range(len(x_t_list)):
                x, y, z = Geometry.enu2ecef(x_t_list[index][0], 
                  x_t_list[index][1], 
                  x_t_list[index][2],
                  reference_lla[0],
                  reference_lla[1],
                  reference_lla[2])
                lat, lon, alt = Geometry.ecef2lla(x, y, z)
                x_t_list[index] = [lat, lon, alt]

            if x_t[0][2] > x_t[1][2]:
                output[target]["points"].append(x_t_list[0])
            else:
                output[target]["points"].append(x_t_list[1])
                
        return output