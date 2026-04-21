import os
import json
import subprocess
import sys
import urllib.request
import time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_FILE = os.path.join(PROJECT_ROOT, "results.json")
SIM_MODULE = os.path.join(PROJECT_ROOT, "simulation_module")

# Store the simulation process
sim_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def get_data():
    if not os.path.exists(RESULTS_FILE):
        return jsonify({"error": "No results yet"}), 404
    try:
        with open(RESULTS_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/network")
def get_network():
    import xml.etree.ElementTree as ET
    net_file = os.path.join(SIM_MODULE, "osm.net.xml")
    lights = []
    if os.path.exists(net_file):
        try:
            tree = ET.parse(net_file)
            root = tree.getroot()
            location = root.find("location")
            if location is not None:
                orig_boundary = location.get("origBoundary", "")
                conv_boundary = location.get("convBoundary", "")
                if orig_boundary and conv_boundary:
                    b = list(map(float, orig_boundary.split(",")))
                    cb = list(map(float, conv_boundary.split(",")))
                    for junc in root.findall("junction"):
                        if junc.get("type") == "traffic_light":
                            x, y = float(junc.get("x", 0)), float(junc.get("y", 0))
                            frac_x = (x - cb[0]) / max(cb[2] - cb[0], 1)
                            frac_y = (y - cb[1]) / max(cb[3] - cb[1], 1)
                            lat = b[1] + frac_y * (b[3] - b[1])
                            lon = b[0] + frac_x * (b[2] - b[0])
                            lights.append({"id": junc.get("id"), "lat": lat, "lon": lon})
        except Exception as e:
            print("Error parsing network:", e)
    return jsonify(lights)


@app.route("/api/launch_sim", methods=["POST"])
def launch_sim():
    global sim_process
    data = request.json or {}
    mode = data.get("mode", "adaptive")
    
    # 1. Kill existing simulation if running
    if sim_process and sim_process.poll() is None:
        sim_process.terminate()
        sim_process.wait()

    try:
        # 2. Launch the AI Simulation Engine
        env = os.environ.copy()
        env["SIM_GUI"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["SIM_MODE"] = mode
        sim_process = subprocess.Popen([sys.executable, os.path.join(SIM_MODULE, "sim_engine.py")], env=env)

        return jsonify({"status": "Simulation launched successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8501, debug=True)
