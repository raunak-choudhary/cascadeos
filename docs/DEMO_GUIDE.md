# CascadeOS Demo Guide

This guide is written to help me run a clear three to five minute demo for judges, recruiters, or technical reviewers.

## Demo Goal

The audience should leave with one clear idea:

CascadeOS shows how graph algorithms, AI agents, live camera signals, and city operations reporting can work together to predict and explain infrastructure cascades.

## Presenter Context

Team name:

```text
Core Catalyst
```

Builder:

```text
Raunak Choudhary
MS Computer Science
New York University
Class of 2026
```

Suggested introduction:

```text
I built CascadeOS as a solo hackathon project under team Core Catalyst to explore how cities could reason about infrastructure failures before they spread. The system connects graph algorithms, multi agent monitoring, real time simulation, Dijkstra rerouting, Claude generated briefings, and YOLO camera signals in one operations dashboard.
```

## Before The Demo

Start backend:

```bash
cd backend
source .venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Start frontend:

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

Open:

```text
http://localhost:5173
```

Recommended browser state:

* Desktop width
* Dark theme
* City Map view
* Backend running without `--reload` if CV is active

## Three Minute Flow

### 1. City Map

Say:

```text
Every node on this map represents a real NYC infrastructure point across water, transit, health, and emergency systems. The graph lets CascadeOS reason about dependencies instead of viewing each system in isolation.
```

Point out:

* Colored nodes by domain
* Larger central nodes
* Node detail panel

### 2. Agents

Switch to Agents.

Say:

```text
Four agents monitor different infrastructure domains. Their alerts flow into a max heap priority queue, so the most severe signals rise to the top first.
```

Point out:

* Water, transit, health, emergency agent cards
* Alert queue visualization
* Reasoning and confidence values

### 3. Simulation

Switch to Simulate.

Choose:

```text
34th St Water Main Break
```

Trigger the cascade.

Say:

```text
This runs a weighted BFS across the infrastructure graph. The system predicts which downstream systems are affected and when.
```

Pause and let the animation run.

Point out:

* Timeline events
* Affected nodes
* Severity colors
* Cascade paths on the map

### 4. Rerouting

Return to City Map after the cascade completes.

Say:

```text
When the cascade affects a transit routing hub, CascadeOS runs Dijkstra over the available graph and excludes blocked nodes. The red dashed line is the original blocked route. The green line is the alternate emergency route.
```

Point out:

* Red blocked route
* Green reroute
* Delay tooltip

### 5. City Briefing

Click:

```text
Generate City Briefing
```

Say:

```text
The briefing is generated for city officials. It combines the cascade state, active alerts, affected systems, and rerouting recommendation into a structured report.
```

Point out:

* Severity banner
* Summary
* Affected systems
* Recommended actions
* Copy report button

### 6. Computer Vision

Switch to CV Feeds.

Say:

```text
CascadeOS also watches NYC DOT camera frames. YOLOv8 detections become alerts and enter the same priority queue as the agent signals.
```

Point out:

* Live camera frames
* Bounding boxes
* Anomaly banner
* Camera marker on map if returning to City Map

## Backup Keyboard Shortcuts

Use these if the UI is already on the right page:

| Key | Action |
| --- | --- |
| `T` | Toggle theme |
| `R` | Reset simulation |
| `Space` | Trigger 34th Street demo cascade |

## If Something Fails

If the map does not load:

* Check `VITE_MAPBOX_TOKEN`
* Refresh the page
* Confirm backend is running

If the briefing fails:

* Check `ANTHROPIC_API_KEY`
* Confirm backend logs do not show an Anthropic authentication error

If CV does not show YOLO:

* Run `pip install -r backend/requirements-ml.txt`
* Confirm `backend/cv/models/yolov8n.pt` exists
* Run the CV smoke test in the root README

If the cascade is already running:

* Press `R`
* Trigger the preset again

## What To Emphasize

For technical judges:

* Weighted BFS was implemented directly for cascade propagation.
* Dijkstra uses NetworkX and excludes blocked nodes.
* Alert priority queue is a max heap.
* 311 surge detection uses a sliding window.
* WebSocket events keep map, graph, alerts, and timeline synchronized.
* YOLO camera detections are not just visual. They become queue alerts.

For product judges:

* The app tells a clear operational story.
* City officials get a briefing, not just raw data.
* Rerouting appears automatically after the cascade.
* Both dark and light themes are supported.
* The system is built for rapid situational awareness.
