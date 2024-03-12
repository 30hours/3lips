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

def interpolate_positions(timestamp_vector, truth_timestamp, truth_position):
    # Convert lists to NumPy arrays for easier manipulation
    truth_timestamp = np.array(truth_timestamp)
    truth_position = np.array(truth_position)

    # Interpolate positions for the new timestamp vector
    interpolated_positions = np.zeros((len(timestamp_vector), truth_position.shape[1]))

    for i in range(truth_position.shape[1]):
        interpolated_positions[:, i] = np.interp(timestamp_vector, truth_timestamp, truth_position[:, i])

    return interpolated_positions

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

    # get LLA coords from first radar
    radar4_lla = [-34.91041, 138.68924, 210]

    # extract data of interest
    server = json_data[0][0]["server"]
    timestamp = []
    position = {}
    detected = {}
    truth_timestamp = []
    truth_position = []
    for item in json_data:

        for method in item:

            if method["server"] != server:
                continue

            if start_time and method["timestamp_event"]/1000 < start_time:
              continue

            if stop_time and method["timestamp_event"]/1000 > stop_time:
              continue

            # store target data
            method_localisation = method["localisation"]

            if method_localisation == "spherical-intersection":
              continue

            if method_localisation not in position:
              position[method_localisation] = {}
              position[method_localisation]["timestamp"] = []
              position[method_localisation]["detections"] = []
            else:
              if args.target_name in method["detections_localised"] and \
              len(method["detections_localised"][args.target_name]["points"]) > 0:
                position[method_localisation]["timestamp"].append(
                  method["timestamp_event"]/1000)
                position[method_localisation]["detections"].append(
                  method["detections_localised"][args.target_name]["points"][0])
                # covert to ENU
                x, y, z = Geometry.lla2ecef(
                  position[method_localisation]["detections"][-1][0],
                  position[method_localisation]["detections"][-1][1],
                  position[method_localisation]["detections"][-1][2])
                x, y, z = Geometry.ecef2enu(x, y, z, radar4_lla[0], 
                  radar4_lla[1], radar4_lla[2])
                if not "detections_enu" in position[method_localisation]:
                  position[method_localisation]["detections_enu"] = []
                position[method_localisation]["detections_enu"].append([x, y, z])

            # store truth data
            if args.target_name in method["truth"]:
                truth_timestamp.append(
                  method["truth"][args.target_name]["timestamp"])
                truth_position.append([
                  method["truth"][args.target_name]["lat"], 
                  method["truth"][args.target_name]["lon"], 
                  method["truth"][args.target_name]["alt"]])

            timestamp.append(method["timestamp_event"])

    # remove duplicates in truth data
    timestamp = list(dict.fromkeys(timestamp))
    timestamp = [element/1000 for element in timestamp]
    truth_timestamp_unique = []
    truth_position_unique = []
    for t, p in zip(truth_timestamp, truth_position):
        if t not in truth_timestamp_unique:
            truth_timestamp_unique.append(t)
            truth_position_unique.append(p)
    truth_timestamp = truth_timestamp_unique
    truth_position = truth_position_unique

    # resample truth to event time (position already sampled correct)
    for i in reversed(range(len(timestamp))):
        if timestamp[i] < min(truth_timestamp) or timestamp[i] > max(truth_timestamp):
            del timestamp[i]
    truth_position_resampled = interpolate_positions(
      timestamp, truth_timestamp, truth_position)

    # convert truth to ENU
    truth_position_resampled_enu = []
    for pos in truth_position_resampled:
        x, y, z = Geometry.lla2ecef(pos[0], pos[1], pos[2])
        truth_position_resampled_enu.append(
          Geometry.ecef2enu(x, y, z, 
          radar4_lla[0], radar4_lla[1], radar4_lla[2]))

    # plot x, y, z
    plt.figure(figsize=(5,7))
    for i in range(3):
        yaxis_truth = [pos[i] for pos in truth_position_resampled_enu]
        plt.subplot(3, 1, i+1)
        plt.plot(timestamp, yaxis_truth, label="ADS-B Truth")
    for method in position:
        for i in range(3):
            yaxis_target = [pos[i] for pos in position[method]["detections_enu"]]
            plt.subplot(3, 1, i+1)
            plt.plot(position[method]["timestamp"], yaxis_target, 'x', label=method)
            plt.xlabel('Timestamp')
            if i == 0:
                plt.ylabel('ENU X (m)')
            if i == 1:
                plt.ylabel('ENU Y (m)')
            if i == 2:
                plt.ylabel('ENU Z (m)')
    
    plt.subplot(3, 1, 1)
    plt.legend()
    plt.tight_layout()
    filename = 'plot_accuracy_' + args.target_name + '.png'
    plt.savefig('save/' + filename, bbox_inches='tight', pad_inches=0.01)

if __name__ == "__main__":
    main()
