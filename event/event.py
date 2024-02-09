import asyncio
import sqlite3
import requests
import threading
import socket
from datetime import datetime

from algorithm.associator.AdsbAssociator import AdsbAssociator
from algorithm.coordreg.EllipseParametric import EllipseParametric
from util.Sqlite import Sqlite

# init db
sqlite = Sqlite('./db/3lips.db')

# init event loop
api = []
api_update = []

async def event():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Event triggered at: " + timestamp, flush=True)

    # main event loop
    #for api_x in api:

      # request data from API
      # response = requests.get(data_i["url_radar_detections"])
      # data_i["radar_detections"] = 

    # API management
    #if sqlite.table_exists('data'):

      # add new API requests
      # rows = sqlite.fetch_all_rows("SELECT * FROM data")
      # for row in rows:
      #     print(row)

      # delete old API requests

      # update output data on db

# event loop
async def main():

    while True:
        await event()
        await asyncio.sleep(1)
        api = api_update

def start_event_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('event', 12345))
        server_socket.listen()

        print("Event listener is waiting for connections...")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received data: {data.decode()}")

if __name__ == "__main__":
    threading.Thread(target=start_event_listener).start()
    asyncio.run(main())