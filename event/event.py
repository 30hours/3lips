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

    # main event loop
    #for api_x in api:

      # request data from API

    # API management

      # add new API requests

      # delete old API requests

      # update output data on db

# event loop
async def main():

    while True:
        await event()
        await asyncio.sleep(1)
        api = api_update

# message received callback
async def callback_message_received(message):
    print(f"Callback: Received message in event.py: {message}", flush=True)

# init messaging
message = Message('event', 6969)
message.set_callback_message_received(callback_message_received)

if __name__ == "__main__":
    threading.Thread(target=message.start_listener).start()
    asyncio.run(main())