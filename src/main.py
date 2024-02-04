# main.py

from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# store state data
servers = [
    {"name": "radar4", "url": "radar4.30hours.dev"},
    {"name": "radar5", "url": "radar5.30hours.dev"}
]
associators = [
  {"name": "ADSB Associator", "id": "adsb-associator"}
]
coordregs = [
  {"name": "Ellipse Analytic Intersection", "id": "ellipse-conic-int"},
  {"name": "Ellipse Parametric", "id": "ellipse-parametric"},
  {"name": "Ellipse Parametric (Arc Length)", "id": "ellipse-parametric-arc"},
  {"name": "Ellipsoid Parametric", "id": "ellipsoid-parametric"},
  {"name": "Ellipsoid Parametric (Arc Length)", "id": "ellipsoid-parametric-arc"}
]

adsbs = [
  {"name": "adsb.30hours.dev", "url": "adsb.30hours.dev"},
  {"name": "None", "url": ""}
]

@app.route("/")
def index():
    return render_template("index.html", servers=servers, \
      associators=associators, coordregs=coordregs, adsbs=adsbs)

# serve static files from the /app/public folder
@app.route('/public/<path:file>')
def serve_static(file):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    public_folder = os.path.join(base_dir, 'public')
    return send_from_directory(public_folder, file)

@app.route("/api")
def api():
    urls = request.args.getlist("url")
    data = [{"url": 'http://' + url} for url in urls]
    return jsonify(data)

@app.route("/map")
def map_page():
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
