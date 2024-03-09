import argparse
import json
from datetime import datetime

def parse_posix_time(value):
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid POSIX time format")

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    
    parser.add_argument("json_string", type=str, help="Input JSON string")
    parser.add_argument("target_name", type=str, help="Target name")
    parser.add_argument("--start_time", type=parse_posix_time, help="Optional start time in POSIX seconds")
    parser.add_argument("--stop_time", type=parse_posix_time, help="Optional stop time in POSIX seconds")

    return parser.parse_args()

def main():
  
    args = parse_command_line_arguments()
    json_data = json.loads(args.json_string)
    start_time = args.start_time if args.start_time else None
    stop_time = args.stop_time if args.stop_time else None
    print("JSON String:", json_data)
    print("Target Name:", args.target_name)
    print("Start Time:", start_time)
    print("Stop Time:", stop_time)

if __name__ == "__main__":
    main()
