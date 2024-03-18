import argparse
import json
import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

from geometry.Geometry import Geometry

def parse_posix_time(value):

  try:
    return int(value)
  except ValueError:
    raise argparse.ArgumentTypeError("Invalid POSIX time format")

def parse_command_line_arguments():

  parser = argparse.ArgumentParser(description="Process command line arguments.")
  parser.add_argument("json_file", type=str, help="Input JSON file path")
  parser.add_argument("target_name", type=str, help="Target name")
  parser.add_argument("--start_time", type=parse_posix_time, help="Optional start time in POSIX seconds")
  parser.add_argument("--stop_time", type=parse_posix_time, help="Optional stop time in POSIX seconds")
  return parser.parse_args()

def main():
  
  # input handling
  args = parse_command_line_arguments()
  json_data = []
  with open(args.json_file, 'r') as json_file:
    for line in json_file:
      try:
        json_object = json.loads(line)
        json_data.append(json_object)
      except json.JSONDecodeError:
        print(f"Error decoding JSON from line: {line}")
  json_data = [item for item in json_data if item]
  start_time = args.start_time if args.start_time else None
  stop_time = args.stop_time if args.stop_time else None
  print("JSON String (Last Non-Empty Data):", json_data[-1])
  print("Target Name:", args.target_name)
  print("Start Time:", start_time)
  print("Stop Time:", stop_time)

  # extract data of interest
  server = json_data[0][0]["server"]
  timestamp = []
  associated = {}
  for item in json_data:
    first_result = item[0]
    if first_result["server"] != server:
      print('error')
      sys.exit(-1)
    if start_time and first_result["timestamp_event"]/1000 < start_time:
      continue
    if stop_time and first_result["timestamp_event"]/1000 > stop_time:
      continue
    # store association data
    if "detections_associated" in first_result:
      if args.target_name in first_result["detections_associated"]:
        for radar in first_result["detections_associated"][args.target_name]:
          if radar['radar'] not in associated:
            associated[radar['radar']] = []
          else:
            associated[radar['radar']].append(first_result["timestamp_event"])
    timestamp.append(first_result["timestamp_event"])

  # data massaging
  timestamp = list(dict.fromkeys(timestamp))
  associated = dict(sorted(associated.items(), key=lambda x: x[0]))
  radars = list(associated.keys())
  radar_label = []
  for radar in radars:
    radar_label.append(radar.split('.', 1)[0])

  # get start and stop times from data
  start_time = min(min(arr) for arr in associated.values())
  stop_time = max(max(arr) for arr in associated.values())
  timestamp = [value for value in timestamp if value >= start_time]
  timestamp = [value for value in timestamp if value <= stop_time]
  
  data = []
  for radar in radars:
    result = [1 if value in associated[radar] else 0 for value in timestamp]
    data.append(result)

  # plot x, y, z
  plt.figure(figsize=(8,4))
  img = plt.imshow(data, aspect='auto', interpolation='none')
  y_extent = plt.gca().get_ylim()
  img.set_extent([start_time/1000, stop_time/1000, y_extent[1], y_extent[0]])
  plt.yticks(np.arange(len(radar_label)), radar_label[::-1], rotation='vertical')
  plt.xlabel('Timestamp')
  plt.ylabel('Radar')
  plt.tight_layout()
  filename = 'plot_associate_' + args.target_name + '.png'
  plt.savefig('save/' + filename, bbox_inches='tight', pad_inches=0.01)

if __name__ == "__main__":
  main()
