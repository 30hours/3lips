"""
@file AdsbTruth.py
@author 30hours
"""

import requests
import math

class AdsbTruth:

    """
    @class AdsbTruth
    @brief A class for storing ADS-B truth in the API response.
    @details Uses truth data in delay-Doppler space from an tar1090 server.
    """

    def __init__(self, seen_pos_limit):

        """
        @brief Constructor for the AdsbTruth class.
        """

        self.seen_pos_limit = seen_pos_limit

    def process(self, server):

        """
        @brief Store ADS-B truth for each target in LLA.
        @param server (str): The tar1090 server to get truth from.
        @return dict: Associated detections by [hex].
        """

        output = {}

        # get tar1090 URL
        url = 'https://' + server + '/data/aircraft.json'

        # get ADSB detections
        try:
            response = requests.get(url, timeout=1)
            response.raise_for_status()
            data = response.json()
            adsb = data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            adsb = None

        # store relevant data
        if adsb:

            # loop over aircraft
            for aircraft in adsb["aircraft"]:

              if aircraft.get("seen_pos") and \
                  aircraft.get("alt_geom") and \
                  aircraft.get("flight") and \
                  aircraft.get("seen_pos") < self.seen_pos_limit:

                      output[aircraft["hex"]] = {}
                      output[aircraft["hex"]]["lat"] = aircraft["lat"]
                      output[aircraft["hex"]]["lon"] = aircraft["lon"]
                      output[aircraft["hex"]]["alt"] = aircraft["alt_geom"]
                      output[aircraft["hex"]]["flight"] = aircraft["flight"]
                      output[aircraft["hex"]]["timestamp"] = \
                        adsb["now"] - aircraft["seen_pos"]

        return output
