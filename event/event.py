import asyncio
import sqlite3
import requests
import threading
import socket
import asyncio
import time
import copy
import json

from algorithm.associator.AdsbAssociator import AdsbAssociator
from algorithm.coordreg.EllipseParametric import EllipseParametric
from common.Message import Message

# init event loop
api = []

# init config
tDelete = 60

async def event():

    global api

    timestamp = int(time.time()*1000)
    print("Event triggered at: " + str(timestamp), flush=True)

    # main event loop
    api_event = copy.copy(api)
    
    for item in api_event:

      print(item)

    # delete old API requests
    api_event = [
      item for item in api_event if timestamp - item["timestamp"] <= tDelete*1000]

    # update API
    api = api_event


# event loop
async def main():

    while True:
        await event()
        await asyncio.sleep(1)

# message received callback
async def callback_message_received(msg):

    print(f"Callback: Received message in event.py: {msg}", flush=True)

    timestamp = int(time.time()*1000)

    # update timestamp if api entry exists
    for x in api:
      if x["url"] == msg:
        x["timestamp"] = timestamp
        break

    # add api entry if does not exist
    if not any(x.get("url") == msg for x in api):
      api.append({})
      api[-1]["url"] = msg
      api[-1]["timestamp"] = timestamp

    # json dump
    output = json.dumps(api)

    return output

# init messaging
message_api_request = Message('event', 6969)
message_api_request.set_callback_message_received(callback_message_received)

if __name__ == "__main__":
    threading.Thread(target=message_api_request.start_listener).start()
    asyncio.run(main())