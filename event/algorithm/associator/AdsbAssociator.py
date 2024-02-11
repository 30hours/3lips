"""
@file AdsbAssociator.py
@author 30hours
"""

class AdsbAssociator:

    """
    @class AdsbAssociator
    @brief A class for associating detections of the same target.
    @details Girst associate ADS-B truth with each radar detection.
    Then associate over multiple radars.
    @see blah2 at https://github.com/30hours/blah2.
    Uses truth data in delay-Doppler space from an adsb2dd server.
    @see adsb2dd at https://github.com/30hours/adsb2dd.
    """

    def __init__(self):

        """
        @brief Constructor for the AdsbAssociator class.
        """

    def process(self, assoc_detections_list):

        """
        @brief Associate detections from 2+ radars.
        @param assoc_detections_list (list): List of JSON associated detections.
        @return str: JSON of associated detections.
        """

    def process_1_radar(self, radar_detections, adsb_detections):

        """
        @brief Associate detections between 1 radar/truth pair.
        @param radar_detections (str): JSON of blah2 radar detections.
        @param adsb_detections (str): JSON of adsb2dd truth detections.
        @return str: JSON of associated detections.
        """

        