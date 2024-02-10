import asyncio
import sqlite3
import requests
import threading
import socket
import asyncio
import time

from algorithm.associator.AdsbAssociator import AdsbAssociator
from algorithm.coordreg.EllipseParametric import EllipseParametric
from common.Message import Message

# init event loop
api = []
api_update = []

async def event():

    timestamp = int(time.time()*1000)
    print("Event triggered at: " + str(timestamp), flush=True)
    print(api)

    # main event loop
    #for api_x in api:

      # request data from API

    # API management

      # add new API requests

      # delete old API requests

      # send output data
      #message_output.send_message(str(int(time.time()*1000)))

# event loop
async def main():

    while True:
        await event()
        await asyncio.sleep(1)
        api = api_update

# message received callback
async def callback_message_received(msg):
    print(f"Callback: Received message in event.py: {msg}", flush=True)
    if msg not in api:
      api.append(msg)
    timestamp = int(time.time()*1000)
    return str(timestamp)

# init messaging
message_api_request = Message('event', 6969)
message_api_request.set_callback_message_received(callback_message_received)
#message_output = Message('api', 6970)

if __name__ == "__main__":
    threading.Thread(target=message_api_request.start_listener).start()
    asyncio.run(main())