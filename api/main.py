"""
@file api.py
@brief API for 3lips.
@author 30hours
"""

from flask import Flask, Response, render_template, request, redirect, jsonify, send_from_directory
import os
import requests
import time
import asyncio

from common.Message import Message

app = Flask(__name__)

# store state data
servers = [
    {"name": "radar4", "url": "radar4.30hours.dev"},
    {"name": "radar5", "url": "radar5.30hours.dev"},
    {"name": "radar6", "url": "radar6.30hours.dev"}
]
associators = [
  {"name": "ADSB Associator", "id": "adsb-associator"}
]
# coordregs = [
#   {"name": "Ellipse Analytic Intersection", "id": "ellipse-conic-int"},
#   {"name": "Ellipse Parametric", "id": "ellipse-parametric"},
#   {"name": "Ellipse Parametric (Arc Length)", "id": "ellipse-parametric-arc"},
#   {"name": "Ellipsoid Parametric", "id": "ellipsoid-parametric"},
#   {"name": "Ellipsoid Parametric (Arc Length)", "id": "ellipsoid-parametric-arc"}
# ]
localisations = [
  {"name": "Ellipsoid Parametric", "id": "ellipsoid-parametric"}
]

adsbs = [
  {"name": "adsb.30hours.dev", "url": "adsb.30hours.dev"},
  {"name": "None", "url": ""}
]

# message received callback
async def callback_message_received(msg):
    print(f"Callback: Received message in main.py: {msg}", flush=True)

# init messaging
message_api_request = Message('event', 6969)

@app.route("/")
def index():
    return render_template("index.html", servers=servers, \
      associators=associators, localisations=localisations, adsbs=adsbs)

# serve static files from the /app/public folder
@app.route('/public/<path:file>')
def serve_static(file):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    public_folder = os.path.join(base_dir, 'public')
    return send_from_directory(public_folder, file)

@app.route("/api")
def api():
    api = request.query_string.decode('utf-8')
    try:
      reply_chunks = message_api_request.send_message(api)
      reply = ''.join(reply_chunks)
      print(reply, flush=True)
      return reply
    except Exception as e:
      reply = "Exception: " + str(e)
      return jsonify(error=reply), 500

@app.route("/map/<path:file>")
def serve_map(file):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    public_folder = os.path.join(base_dir, 'map')
    return send_from_directory(public_folder, file)

# handle /cesium/ specifically
@app.route('/cesium/')
def serve_cesium_index():
    return redirect('/cesium/index.html')

@app.route('/cesium/<path:file>')
def serve_cesium_content(file):
    apache_url = 'http://cesium-apache/' + file
    try:
        response = requests.get(apache_url)
        if response.status_code == 200:
            return Response(response.content, content_type=response.headers['content-type'])
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from Apache server: {e}")
    return Response('Error fetching content from Apache server', status=500, content_type='text/plain')

if __name__ == "__main__":
    app.run()
