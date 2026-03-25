# 🚦 TrafficFlow AI – GreenWave

> **AI-powered adaptive traffic signal control system** combining real-time computer vision (YOLOv8) with microscopic traffic simulation (SUMO) to reduce congestion and optimize signal timings.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Modules](#modules)
  - [Vision Module](#vision-module)
  - [Simulation Module](#simulation-module)
  - [Data](#data)
  - [SUMO Network Build](#sumo-network-build)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)
- [Performance Metrics](#performance-metrics)
- [Configuration](#configuration)
- [License](#license)

---

## Overview

TrafficFlow AI – GreenWave is a two-module system designed to tackle urban traffic congestion:

| Module | Purpose | Key Technology |
|--------|---------|----------------|
| **Vision Module** | Real-time vehicle detection & counting from video feeds | YOLOv8 + FastAPI |
| **Simulation Module** | Microscopic traffic simulation with adaptive signal control | SUMO + TraCI |

The vision module processes live traffic camera footage to detect and count vehicles, while the simulation module uses SUMO (Simulation of Urban MObility) to model real-world road networks and adaptively control traffic light timings based on vehicle density.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   TrafficFlow AI – GreenWave            │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│   VISION MODULE      │     SIMULATION MODULE            │
│                      │                                  │
│  ┌────────────────┐  │  ┌────────────────────────────┐  │
│  │ traffic.mp4    │  │  │  OSM Road Network (.osm)   │  │
│  │ (Video Feed)   │  │  │  ↓                         │  │
│  │      ↓         │  │  │  NETCONVERT → .net.xml     │  │
│  │ YOLOv8 Model   │  │  │  ↓                         │  │
│  │ (yolov8n.pt)   │  │  │  randomTrips → .rou.xml    │  │
│  │      ↓         │  │  │  ↓                         │  │
│  │ Vehicle Count  │  │  │  SUMO Simulation Engine     │  │
│  │      ↓         │  │  │  ↓                         │  │
│  │ FastAPI REST   │──│──│  TraCI (Adaptive Control)   │  │
│  │ /get_traffic_  │  │  │  ↓                         │  │
│  │    count       │  │  │  Performance Metrics        │  │
│  └────────────────┘  │  └────────────────────────────┘  │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
```

---

## Project Structure

```
TrafficFlow-AI-GreenWave-main/
│
├── vision_module/               # Computer vision subsystem
│   ├── vision_api.py            # FastAPI server for vehicle detection
│   ├── show_video.py            # Real-time annotated video viewer
│   └── yolov8n.pt               # Pre-trained YOLOv8 Nano model
│
├── simulation_module/           # Traffic simulation subsystem
│   ├── sim_engine.py            # Main simulation engine (adaptive/static)
│   ├── osm.sumocfg              # SUMO simulation configuration
│   ├── osm.net.xml              # Road network definition
│   ├── osm.rou.xml              # Vehicle route definitions
│   ├── osm.trips.xml            # Trip definitions
│   ├── map.osm                  # Original OpenStreetMap data
│   ├── test_tls.py              # Traffic light discovery test
│   ├── test2.py                 # Manual signal override test (RED/GREEN)
│   └── tls_force_test.py        # Phase forcing test
│
├── data/
│   └── traffic.mp4              # Sample traffic video (~59 MB)
│
└── 2026-02-25-00-09-38/         # SUMO network build artifacts
    ├── build.bat                # Trip generation script
    ├── run.bat                  # SUMO GUI launch script
    ├── osm.sumocfg              # Full SUMO config with output settings
    ├── osm.net.xml.gz           # Compressed road network
    ├── osm.passenger.trips.xml  # Generated passenger trips
    ├── osm.poly.xml.gz          # Polygon data (buildings, etc.)
    ├── output.add.xml           # Additional output configuration
    ├── edgeData.xml             # Edge-level traffic data
    ├── tripinfos.xml            # Per-trip statistics
    └── stats.xml                # Aggregate simulation statistics
```

---

## Modules

### Vision Module

The vision module provides real-time vehicle detection using **YOLOv8** (You Only Look Once v8) and serves results through a **FastAPI** REST API.

#### `vision_api.py` — FastAPI Vehicle Detection Server

- **Framework:** FastAPI
- **Model:** YOLOv8 Nano (`yolov8n.pt`) from Ultralytics
- **Input:** Reads frames from `data/traffic.mp4`
- **Detection Classes:**
  - Class `2` — Car
  - Class `5` — Bus
  - Class `7` — Truck

**Congestion Classification Logic:**

| Vehicle Count | Status |
|:---:|:---:|
| > 15 | 🔴 High Congestion |
| 8–15 | 🟡 Moderate |
| ≤ 7 | 🟢 Clear |

The API loops through the video file and automatically resets to the beginning when all frames have been read.

#### `show_video.py` — Real-Time Video Viewer

A standalone script that opens the traffic video and displays YOLOv8 detection results in a window with bounding boxes drawn on detected vehicles. Press `q` to quit.

---

### Simulation Module

The simulation module runs a **SUMO** (Simulation of Urban MObility) microscopic traffic simulation controlled via the **TraCI** Python interface.

#### `sim_engine.py` — Main Simulation Engine

This is the core simulation engine. It supports two operating modes:

| Mode | Behavior |
|:---:|:---:|
| **`adaptive`** | Dynamically adjusts traffic light phase durations based on real-time vehicle density (every 20 seconds) |
| **`static`** | Uses default/fixed signal timings from the network file |

**`TrafficController` Class:**

```python
class TrafficController:
    def __init__(self, tl_id)          # Bind to a traffic light
    def get_vehicle_density(self)       # Count vehicles on controlled lanes
    def optimize_signal(self, count)    # Set phase duration based on density
```

**Adaptive Signal Timing Rules:**

| Vehicles on Controlled Lanes | Green Phase Duration |
|:---:|:---:|
| > 20 | 50 seconds |
| 11–20 | 35 seconds |
| ≤ 10 | 20 seconds |

**Performance Tracking:**
- Counts total simulation delay (seconds where vehicle speed < 0.1 m/s)
- Tracks unique vehicles that entered the simulation
- Computes average delay per vehicle

#### Test Scripts

| Script | Purpose |
|--------|---------|
| `test_tls.py` | Verifies SUMO can load the network and discovers traffic light IDs |
| `test2.py` | Tests manual signal override — forces RED then GREEN states via `setRedYellowGreenState()` |
| `tls_force_test.py` | Tests phase-level control — forces specific traffic light phases via `setPhase()` |

#### SUMO Configuration (`osm.sumocfg`)

```xml
<configuration>
    <input>
        <net-file value="osm.net.xml"/>
        <route-files value="osm.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="2000"/>
    </time>
</configuration>
```

Simulates 2,000 seconds of traffic on the imported OpenStreetMap road network.

---

### Data

| File | Description | Size |
|------|-------------|:---:|
| `traffic.mp4` | Sample traffic camera footage used by the vision module | ~59 MB |

---

### SUMO Network Build

The `2026-02-25-00-09-38/` directory contains the full SUMO scenario generated from OpenStreetMap data:

**Build Pipeline:**
1. **OSM export** → `osm_bbox.osm.xml.gz` (raw map data)
2. **NETCONVERT** → `osm.net.xml.gz` (road network with traffic lights)
3. **randomTrips.py** → `osm.passenger.trips.xml` (synthetic vehicle demand)
4. **SUMO simulation** → `tripinfos.xml`, `stats.xml`, `edgeData.xml` (outputs)

**Key Build Parameters** (from `build.bat`):
- Insertion density: **12 vehicles/km/lane**
- Simulation period: **0–3600 seconds** (1 hour)
- Min trip distance: **300 m**
- Vehicle class: **passenger** only
- Random seed: **42** (reproducible results)

---

## Prerequisites

| Dependency | Version | Purpose |
|------------|---------|---------|
| **Python** | ≥ 3.8 | Runtime |
| **SUMO** | ≥ 1.26.0 | Traffic simulation engine |
| **FastAPI** | Latest | REST API framework |
| **Uvicorn** | Latest | ASGI server |
| **Ultralytics** | Latest | YOLOv8 model inference |
| **OpenCV** | Latest | Video frame processing |
| **TraCI** | (bundled with SUMO) | Python ↔ SUMO interface |

> **Important:** The `SUMO_HOME` environment variable must be set and point to your SUMO installation directory.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/TrafficFlow-AI-GreenWave.git
cd TrafficFlow-AI-GreenWave-main

# 2. Install Python dependencies
pip install fastapi uvicorn ultralytics opencv-python

# 3. Set SUMO_HOME (example for macOS/Linux)
export SUMO_HOME="/path/to/sumo"

# 4. Verify SUMO installation
sumo --version
```

---

## Usage

### 1. Run the Vision API

```bash
cd vision_module
uvicorn vision_api:app --reload --port 8000
```

Then open:
- **Swagger Docs:** http://localhost:8000/docs
- **Vehicle Count API:** http://localhost:8000/get_traffic_count

### 2. View Annotated Video

```bash
cd vision_module
python show_video.py
```

Press **`q`** to quit the video window.

### 3. Run the Traffic Simulation

```bash
cd simulation_module
python sim_engine.py
```

To switch between **adaptive** and **static** modes, edit `MODE` in `sim_engine.py`:

```python
MODE = "adaptive"   # or "static"
```

### 4. Run Test Scripts

```bash
# Discover traffic lights
python test_tls.py

# Test manual signal override (requires sumo-gui)
python test2.py

# Test phase forcing (requires sumo-gui)
python tls_force_test.py
```

---

## API Reference

### `GET /`

Health check endpoint.

**Response:**
```json
{
  "message": "Vision API is running. Go to /docs to test it."
}
```

### `GET /get_traffic_count`

Returns real-time vehicle count and congestion status from the current video frame.

**Response:**
```json
{
  "intersection": "Main_Street_Cam",
  "timestamp": "Live",
  "vehicle_count": 12,
  "status": "Moderate"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `intersection` | string | Camera/intersection identifier |
| `timestamp` | string | Always `"Live"` for real-time feeds |
| `vehicle_count` | integer | Number of detected vehicles (cars, buses, trucks) |
| `status` | string | `"Clear"`, `"Moderate"`, or `"High Congestion"` |

---

## How It Works

### Vision Pipeline

1. **Frame Capture** — Reads one frame at a time from `traffic.mp4`
2. **YOLOv8 Inference** — Runs the frame through `yolov8n.pt` filtering for COCO classes 2 (car), 5 (bus), 7 (truck)
3. **Counting** — Counts bounding boxes returned by the model
4. **Classification** — Maps vehicle count to congestion level
5. **API Response** — Returns JSON with intersection ID, count, and status

### Simulation Pipeline

1. **Network Loading** — SUMO loads the OSM-derived road network (`.net.xml`) and vehicle routes (`.rou.xml`)
2. **Simulation Loop** — Steps through the simulation one second at a time
3. **Density Measurement** — Every 20 seconds (in adaptive mode), the `TrafficController` counts vehicles on lanes controlled by each traffic light
4. **Signal Optimization** — Adjusts green phase duration proportionally to detected vehicle density
5. **Metric Collection** — Tracks per-vehicle delay (time spent at speed < 0.1 m/s)
6. **Summary** — Prints total vehicles, total delay, and average delay per vehicle

---

## Performance Metrics

The simulation engine outputs a performance summary comparing adaptive vs. static modes:

```
===== PERFORMANCE SUMMARY =====
Mode: adaptive
Total Vehicles: 1234
Total System Delay: 56789
Average Delay per Vehicle: 46.02
```

Run both modes and compare to quantify the improvement:

```bash
# Edit MODE = "adaptive" → run → note metrics
# Edit MODE = "static"   → run → note metrics
```

---

## Configuration

### Simulation Parameters

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| `MODE` | `sim_engine.py:26` | `"adaptive"` | Control mode: `"adaptive"` or `"static"` |
| Simulation duration | `osm.sumocfg` | 2000s | `<end value="2000"/>` |
| High-density threshold | `sim_engine.py:68` | 20 vehicles | Triggers 50s green phase |
| Mid-density threshold | `sim_engine.py:70` | 10 vehicles | Triggers 35s green phase |
| Optimization interval | `sim_engine.py:106` | Every 20s | How often signal timings are recalculated |

### Vision Parameters

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| Detection classes | `vision_api.py:26` | `[2, 5, 7]` | COCO class IDs (car, bus, truck) |
| High congestion threshold | `vision_api.py:29` | > 15 | Vehicle count for "High Congestion" |
| Moderate threshold | `vision_api.py:29` | > 7 | Vehicle count for "Moderate" |

---

## License

This project is provided for educational and research purposes.
