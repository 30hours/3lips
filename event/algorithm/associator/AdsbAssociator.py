"""
@file AdsbAssociator.py
@author 30hours
"""

import requests

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

    def process(self, radar_list, radar_data):

        """
        @brief Associate detections from 2+ radars.
        @param radar_list (list): List of radars to associate.
        @param radar_data (dict): Radar data for list of radars.
        @return dict: Associated detections by [hex][radar].
        """

        assoc_detections = {}

        for radar in radar_list:

          if radar_data[radar]["config"] is not None:

            # get URL for adsb2truth
            url = self.generate_api_url(radar, radar_data[radar])

            # get ADSB detections
            try:
                response = requests.get(url, timeout=1)
                response.raise_for_status()
                data = response.json()
                adsb_detections = data
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data from {url}: {e}")
                adsb_detections = None

            # associate radar and truth
            print(adsb_detections, flush=True)



        #print(radar_list, flush=True)
        #print(radar_data, flush=True)



    def process_1_radar(self, radar_detections, adsb_detections):

        """
        @brief Associate detections between 1 radar/truth pair.
        @param radar_detections (str): JSON of blah2 radar detections.
        @param adsb_detections (str): JSON of adsb2dd truth detections.
        @return str: JSON of associated detections.
        """

    def generate_api_url(self, radar, radar_data):

        """
        @brief Generate an adsb2dd API endpoint for each radar.
        @see adsb2dd at https://github.com/30hours/adsb2dd.
        @param radar (str): Radar to run adsb2dd.
        @param radar_data (dict): Radar data for this radar.
        @return str: adsb2dd API for radar.
        """

        rx_lat = radar_data['config']['location']['rx']['latitude']
        rx_lon = radar_data['config']['location']['rx']['longitude']
        rx_alt = radar_data['config']['location']['rx']['altitude']
        tx_lat = radar_data['config']['location']['tx']['latitude']
        tx_lon = radar_data['config']['location']['tx']['longitude']
        tx_alt = radar_data['config']['location']['tx']['altitude']
        fc = radar_data['config']['capture']['fc']
        adsb = radar_data['config']['truth']['adsb']['ip']

        api_url = "http://adsb2dd.30hours.dev/api/dd"

        api_query = (
            api_url +
            "?rx=" + str(rx_lat) + "," + 
            str(rx_lon) + "," + 
            str(rx_alt) +
            "&tx=" + str(tx_lat) + "," + 
            str(tx_lon) + "," + 
            str(tx_alt) +
            "&fc=" + str(fc) +
            "&server=" + "http://" + str(adsb)
        )

        return api_query
