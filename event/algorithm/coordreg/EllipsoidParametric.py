"""
@file EllipsoidParametric.py
@author 30hours
"""

from data.Ellipsoid import Ellipsoid

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

    def process(self, assoc_detections, radar_data):

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
        