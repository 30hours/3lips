"""
@file event.py
@brief Event loop for 3lips.
@author 30hours
"""

import asyncio
import requests
import threading
import asyncio
import time
import copy
import json
import hashlib
import os
import yaml

from algorithm.associator.AdsbAssociator import AdsbAssociator
from algorithm.localisation.EllipseParametric import EllipseParametric
from algorithm.localisation.EllipsoidParametric import EllipsoidParametric
from algorithm.localisation.SphericalIntersection import SphericalIntersection
from algorithm.truth.AdsbTruth import AdsbTruth
from common.Message import Message
from data.Ellipsoid import Ellipsoid
from algorithm.geometry.Geometry import Geometry

# init config file
try:
  with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)
  nSamplesEllipse = config['localisation']['ellipse']['nSamples']
  thresholdEllipse = config['localisation']['ellipse']['threshold']
  nDisplayEllipse = config['localisation']['ellipse']['nDisplay']
  nSamplesEllipsoid = config['localisation']['ellipsoid']['nSamples']
  thresholdEllipsoid = config['localisation']['ellipsoid']['threshold']
  nDisplayEllipsoid = config['localisation']['ellipsoid']['nDisplay']
  tDeleteAdsb = config['associate']['adsb']['tDelete']
  save = config['3lips']['save']
  tDelete = config['3lips']['tDelete']
except FileNotFoundError:
  print("Error: Configuration file not found.")
except yaml.YAMLError as e:
  print("Error reading YAML configuration:", e)

# init event loop
api = []

# init config
tDelete = tDelete
adsbAssociator = AdsbAssociator()
ellipseParametricMean = EllipseParametric("mean", nSamplesEllipse, thresholdEllipse)
ellipseParametricMin = EllipseParametric("min", nSamplesEllipse, thresholdEllipse)
ellipsoidParametricMean = EllipsoidParametric("mean", nSamplesEllipsoid, thresholdEllipsoid)
ellipsoidParametricMin = EllipsoidParametric("min", nSamplesEllipsoid, thresholdEllipsoid)
sphericalIntersection = SphericalIntersection()
adsbTruth = AdsbTruth(tDeleteAdsb)
saveFile = '/app/save/' + str(int(time.time())) + '.ndjson'

async def event():

  print('Start event', flush=True)

  global api, save
  timestamp = int(time.time()*1000)
  api_event = copy.copy(api)

  # list all blah2 radars
  radar_names = []
  for item in api_event:
    for radar in item["server"]:
      radar_names.append(radar)
  radar_names = list(set(radar_names))

  # get detections all radar
  radar_detections_url = [
    "http://" + radar_name + "/api/detection" for radar_name in radar_names]
  radar_detections = []
  for url in radar_detections_url:
    try:
      response = requests.get(url, timeout=1)
      response.raise_for_status()
      data = response.json()
      radar_detections.append(data)
    except requests.exceptions.RequestException as e:
      print(f"Error fetching data from {url}: {e}")
      radar_detections.append(None)

  # get config all radar
  radar_config_url = [
    "http://" + radar_name + "/api/config" for radar_name in radar_names]
  radar_config = []
  for url in radar_config_url:
    try:
      response = requests.get(url, timeout=1)
      response.raise_for_status()
      data = response.json()
      radar_config.append(data)
    except requests.exceptions.RequestException as e:
      print(f"Error fetching data from {url}: {e}")
      radar_config.append(None)

  # store detections in dict
  radar_dict = {}
  for i in range(len(radar_names)):
    radar_dict[radar_names[i]] = {
      "detection": radar_detections[i],
      "config": radar_config[i]
    }

  # store truth in dict
  truth_adsb = {}
  adsb_urls = []
  for item in api_event:
    adsb_urls.append(item["adsb"])
  adsb_urls = list(set(adsb_urls))
  for url in adsb_urls:
    truth_adsb[url] = adsbTruth.process(url)

  # main processing
  for item in api_event:

    start_time = time.time()

    # extract dict for item
    radar_dict_item =  {
      key: radar_dict[key] 
      for key in item["server"] 
      if key in radar_dict
    }

    # associator selection
    if item["associator"] == "adsb-associator":
      associator = adsbAssociator
    else:
      print("Error: Associator invalid.")
      return

    # localisation selection
    if item["localisation"] == "ellipse-parametric-mean":
      localisation = ellipseParametricMean
    elif item["localisation"] == "ellipse-parametric-min":
      localisation = ellipseParametricMin
    elif item["localisation"] == "ellipsoid-parametric-mean":
      localisation = ellipsoidParametricMean
    elif item["localisation"] == "ellipsoid-parametric-min":
      localisation = ellipsoidParametricMin
    elif item["localisation"] == "spherical-intersection":
      localisation = sphericalIntersection
    else:
      print("Error: Localisation invalid.")
      return

    # processing
    associated_dets = associator.process(item["server"], radar_dict_item, timestamp)
    associated_dets_3_radars = {
      key: value
      for key, value in associated_dets.items()
      if isinstance(value, list) and len(value) >= 3
    }
    if associated_dets_3_radars:
      print('Detections from 3 or more radars availble.')
      print(associated_dets_3_radars)
    associated_dets_2_radars = {
      key: value
      for key, value in associated_dets.items()
      if isinstance(value, list) and len(value) >= 2
    }
    localised_dets = localisation.process(associated_dets_3_radars, radar_dict_item)

    if associated_dets:
      print(associated_dets, flush=True)

    # show ellipsoids of associated detections for 1 target
    ellipsoids = {}
    if item["localisation"] == "ellipse-parametric-mean" or \
    item["localisation"] == "ellipsoid-parametric-mean" or \
    item["localisation"] == "ellipse-parametric-min" or \
    item["localisation"] == "ellipsoid-parametric-min":
      if associated_dets_2_radars:
        # get first target key
        key = next(iter(associated_dets_2_radars))
        ellipsoid_radars = []
        for radar in associated_dets_2_radars[key]:
          ellipsoid_radars.append(radar["radar"])
          x_tx, y_tx, z_tx = Geometry.lla2ecef(
            radar_dict_item[radar["radar"]]["config"]['location']['tx']['latitude'],
            radar_dict_item[radar["radar"]]["config"]['location']['tx']['longitude'],
            radar_dict_item[radar["radar"]]["config"]['location']['tx']['altitude']
          )
          x_rx, y_rx, z_rx = Geometry.lla2ecef(
            radar_dict_item[radar["radar"]]["config"]['location']['rx']['latitude'],
            radar_dict_item[radar["radar"]]["config"]['location']['rx']['longitude'],
            radar_dict_item[radar["radar"]]["config"]['location']['rx']['altitude']
          )
          ellipsoid = Ellipsoid(
            [x_tx, y_tx, z_tx],
            [x_rx, y_rx, z_rx],
            radar["radar"]
          )
          points = localisation.sample(ellipsoid, radar["delay"]*1000, nDisplayEllipse)
          for i in range(len(points)):
            lat, lon, alt = Geometry.ecef2lla(points[i][0], points[i][1], points[i][2])
            if item["localisation"] == "ellipsoid-parametric-mean" or \
            item["localisation"] == "ellipsoid-parametric-min":
              alt = round(alt)
            if item["localisation"] == "ellipse-parametric-mean" or \
            item["localisation"] == "ellipse-parametric-min":
              alt = 0
            points[i] = ([round(lat, 3), round(lon, 3), alt])
          ellipsoids[radar["radar"]] = points

    stop_time = time.time()

    # output data to API
    item["timestamp_event"] = timestamp
    item["truth"] = truth_adsb[item["adsb"]]
    item["detections_associated"] = associated_dets
    item["detections_localised"] = localised_dets
    item["ellipsoids"] = ellipsoids
    item["time"] = stop_time - start_time

    print('Method: ' + item["localisation"], flush=True)
    print(item["time"], flush=True)

  # delete old API requests
  api_event = [
    item for item in api_event if timestamp - item["timestamp"] <= tDelete*1000]

  # update API
  api = api_event

  # save to file
  if save:
    append_api_to_file(api)


# event loop
async def main():

  while True:
    await event()
    await asyncio.sleep(1)

def append_api_to_file(api_object, filename=saveFile):

  if not os.path.exists(filename):
    with open(filename, 'w') as new_file:
      pass

  with open(filename, 'a') as json_file:
    json.dump(api_object, json_file)
    json_file.write('\n')

def short_hash(input_string, length=10):

  hash_object = hashlib.sha256(input_string.encode())
  short_hash = hash_object.hexdigest()[:length]
  return short_hash

# message received callback
async def callback_message_received(msg):

  timestamp = int(time.time()*1000)

  # update timestamp if API entry exists
  for x in api:
    if x["hash"] == short_hash(msg):
      x["timestamp"] = timestamp
      break

  # add API entry if does not exist, split URL
  if not any(x.get("hash") == short_hash(msg) for x in api):
    api.append({})
    api[-1]["hash"] = short_hash(msg)
    url_parts = msg.split("&")
    for part in url_parts:
      key, value = part.split("=")
      if key in api[-1]:
        if not isinstance(api[-1][key], list):
          api[-1][key] = [api[-1][key]]
        api[-1][key].append(value)
      else:
        api[-1][key] = value
    api[-1]["timestamp"] = timestamp
    if not isinstance(api[-1]["server"], list):
      api[-1]["server"] = [api[-1]["server"]]

  # json dump
  for item in api:
    if item["hash"] == short_hash(msg):
      output = json.dumps(item)
      break

  return output

# init messaging
message_api_request = Message('event', 6969)
message_api_request.set_callback_message_received(callback_message_received)

if __name__ == "__main__":
  threading.Thread(target=message_api_request.start_listener).start()
  asyncio.run(main())
