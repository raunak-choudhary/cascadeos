# CascadeOS Backend

The CascadeOS backend is a FastAPI service that powers graph data, simulations, agent alerts, rerouting, city briefings, WebSocket events, and computer vision signals.

Core Catalyst built this backend to act as the reasoning layer for the project. It owns the infrastructure graph, the cascade algorithms, the agent queue, and all external city data integrations.

## What The Backend Does

* Serves infrastructure graph nodes and edges
* Computes betweenness centrality
* Runs weighted BFS cascade prediction
* Runs Dijkstra rerouting for emergency movement
* Generates city briefings with Claude Sonnet
* Runs four infrastructure monitoring agents
* Maintains a max heap alert priority queue
* Connects to NYC DOT camera feeds
* Runs YOLOv8 detections on live camera frames
* Broadcasts real time events over WebSockets

## Main Files

```text
backend/
  main.py                         FastAPI app entry point
  config.py                       Environment loading with pydantic settings
  routers/ws.py                   WebSocket connection manager
  routers/graph.py                Infrastructure graph API
  routers/simulation.py           Cascade trigger and reset API
  routers/briefing.py             City briefing API
  routers/cv.py                   Computer vision API and polling loop
  graph/infrastructure_graph.py   40 node NYC graph
  graph/cascade_bfs.py            Weighted BFS cascade engine
  graph/dijkstra_reroute.py       Emergency rerouting
  agents/                         Domain agents and orchestrator
  cv/camera_client.py             NYC DOT camera client
  cv/yolo_detector.py             YOLOv8 detector wrapper
```

## Requirements

Required:

* Python 3.12
* FastAPI
* NetworkX
* Anthropic SDK
* httpx
* aiohttp
* pydantic settings

Optional but needed for true CV inference:

* torch
* torch geometric
* ultralytics
* opencv
* Pillow

## Setup

From the repo root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Install ML dependencies for the full Phase 5 demo:

```bash
pip install -r requirements-ml.txt
```

## Environment

Create the backend env file:

```bash
cp .env.example .env
```

Fill in:

```text
ANTHROPIC_API_KEY=
NYC_OPEN_DATA_APP_TOKEN=
NYC_311_ENDPOINT=https://data.cityofnewyork.us/resource/erm2-nwe9.json
NYC_DOT_CAMERA_API_URL=https://webcams.nyctmc.org/api/cameras
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173
APP_ENV=development
MODEL_CHECKPOINT_PATH=./ml/checkpoints/tgnn_latest.pt
YOLO_MODEL_PATH=./cv/models/yolov8n.pt
ENABLE_CV=true
ENABLE_TGNN=true
CASCADE_PLAYBACK_SPEED=1.0
CV_POLL_INTERVAL=30
```

The backend intentionally fails early if required environment variables are missing.

## Model Weights

The YOLO model path is:

```text
backend/cv/models/yolov8n.pt
```

If the weights are missing after cloning, download YOLOv8n from Ultralytics and place it at that path. The model file is not meant to be committed to GitHub.

## Run Locally

```bash
source .venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs:

```text
http://localhost:8000/docs
```

## Verification

Import check:

```bash
python -c "from main import app; print('OK')"
```

Route check:

```bash
python - <<'PY'
from main import app
print([route.path for route in app.routes])
PY
```

CV check:

```bash
python - <<'PY'
import asyncio
from routers.cv import poll_cv_once

async def main():
    results = await poll_cv_once()
    print(results[0]["model_status"] if results else "no cameras")

asyncio.run(main())
PY
```

Expected value with ML installed:

```text
yolo
```

## API Overview

Graph:

```text
GET /graph/nodes
GET /graph/edges
GET /graph/stats
GET /graph/reroute
```

Simulation:

```text
POST /simulation/trigger
POST /simulation/reset
GET /simulation/scenarios
GET /simulation/status
```

Briefing:

```text
POST /briefing/generate
```

Computer vision:

```text
GET /cv/cameras
GET /cv/latest
POST /cv/poll
GET /cv/latest-frame/{camera_id}
```

WebSocket:

```text
WS /ws/main
```

## WebSocket Events

The backend broadcasts:

* `heartbeat`
* `agent_update`
* `alert`
* `queue_snapshot`
* `311_surge`
* `cascade_start`
* `cascade_node`
* `cascade_complete`
* `simulation_reset`
* `reroute_update`
* `cv_update`
* `cv_status`

## Development Notes

Use `python`, not `python3`, on the project machine. The intended interpreter is conda Python 3.12.

For demos with CV enabled, running without `--reload` can be cleaner because file watchers may react to large package changes inside `.venv`.

The backend keeps real secrets out of source control. Never commit `.env`.
