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
import yaml

from common.Message import Message

app = Flask(__name__)

# init config file
try:
  with open('config/config.yml', 'r') as file:
      config = yaml.safe_load(file)
  radar_data = config['radar']
  map_data = config['map']
  config_data = config
except FileNotFoundError:
  print("Error: Configuration file not found.")
except yaml.YAMLError as e:
  print("Error reading YAML configuration:", e)

# store state data
servers = []
for radar in radar_data:
  if radar['name'] and radar['url']:
    servers.append({'name': radar['name'], 'url': radar['url']})

associators = [
  {"name": "ADSB Associator", "id": "adsb-associator"}
]

localisations = [
  {"name": "Ellipse Parametric (Mean)", "id": "ellipse-parametric-mean"},
  {"name": "Ellipse Parametric (Min)", "id": "ellipse-parametric-min"},
  {"name": "Ellipsoid Parametric (Mean)", "id": "ellipsoid-parametric-mean"},
  {"name": "Ellipsoid Parametric (Min)", "id": "ellipsoid-parametric-min"},
  {"name": "Spherical Intersection", "id": "spherical-intersection"}
]

adsbs = [
  {"name": map_data['tar1090'], "url": map_data['tar1090']},
  {"name": "None", "url": ""}
]

# store valid ids
valid = {}
valid['servers'] = [item['url'] for item in servers]
valid['associators'] = [item['id'] for item in associators]
valid['localisations'] = [item['id'] for item in localisations]
valid['adsbs'] = [item['url'] for item in adsbs]

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
  # input protection
  servers_api = request.args.getlist('server')
  associators_api = request.args.getlist('associator')
  localisations_api = request.args.getlist('localisation')
  adsbs_api = request.args.getlist('adsb')
  if not all(item in valid['servers'] for item in servers_api):
    return 'Invalid server'
  if not all(item in valid['associators'] for item in associators_api):
    return 'Invalid associator'
  if not all(item in valid['localisations'] for item in localisations_api):
    return 'Invalid localisation'
  if not all(item in valid['adsbs'] for item in adsbs_api):
    return 'Invalid ADSB'
  # send to event handler
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

# output config file
@app.route('/config')
def config():
  return config_data

if __name__ == "__main__":
  app.run()
