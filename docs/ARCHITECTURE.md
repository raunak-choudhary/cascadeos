# CascadeOS Architecture

This document explains how CascadeOS is organized and how data moves through the system.

Core Catalyst built CascadeOS as a full stack city operations dashboard. The backend reasons over infrastructure signals. The frontend turns those signals into an interactive command center.

## System Overview

```text
NYC Open Data
NYC DOT Cameras
Claude Sonnet
        |
        v
FastAPI backend
        |
        v
WebSocket and REST APIs
        |
        v
React frontend
```

## Backend Responsibilities

The backend owns:

* Infrastructure graph
* Graph algorithms
* Agent orchestration
* Alert priority queue
* City briefing generation
* Computer vision polling
* WebSocket broadcasting

Important modules:

```text
backend/main.py
backend/config.py
backend/routers/
backend/agents/
backend/graph/
backend/cv/
backend/utils/
```

## Frontend Responsibilities

The frontend owns:

* City map rendering
* System graph rendering
* Agent panel
* Alert feed
* Simulation controls
* Cascade timeline
* City briefing panel
* CV camera panel
* Theme and responsive layout

Important modules:

```text
frontend/src/App.jsx
frontend/src/components/
frontend/src/context/
frontend/src/services/api.js
frontend/src/theme/
frontend/src/styles/
```

## Provider Order

The provider order is intentional:

```text
ThemeProvider
  AgentProvider
    CascadeProvider
      GraphProvider
        AppShell
```

Why this matters:

* Theme data must be available everywhere.
* Agent state receives alerts, queue updates, and CV events.
* Cascade state receives simulation and reroute events.
* Graph state is used by map and graph views inside the shell.

## Data Flow

### Agent Flow

```text
External data
  -> domain agent
  -> Claude analysis
  -> alert queue
  -> WebSocket alert
  -> frontend alert feed and agent panel
```

### Cascade Flow

```text
User triggers failure
  -> POST /simulation/trigger
  -> weighted BFS
  -> cascade_start
  -> cascade_node events
  -> cascade_complete
  -> Dijkstra reroute
  -> reroute_update
```

### Briefing Flow

```text
User clicks Generate City Briefing
  -> POST /briefing/generate
  -> current cascade state
  -> active alerts
  -> reroute recommendation
  -> Claude Sonnet
  -> structured report
```

### Computer Vision Flow

```text
NYC DOT camera API
  -> camera client
  -> latest JPEG frame
  -> YOLOv8 detector
  -> cv_update WebSocket event
  -> alert queue if anomaly is active
  -> frontend CV panel and map marker
```

## Algorithms

Weighted BFS:

* Implemented in `backend/graph/cascade_bfs.py`
* Predicts downstream cascade impact
* Uses propagation time and severity decay

Dijkstra:

* Implemented in `backend/graph/dijkstra_reroute.py`
* Uses NetworkX
* Excludes blocked nodes
* Returns original route, alternate route, added delay, and recommendation

Max heap alert queue:

* Implemented in `backend/utils/priority_queue.py`
* Uses Python `heapq`
* Stores higher severity alerts first

Sliding window:

* Implemented in `backend/data/sliding_window_311.py`
* Detects local complaint surges over time

YOLOv8:

* Implemented in `backend/cv/yolo_detector.py`
* Runs object detection on traffic camera frames
* Converts visual detections into city operations signals

## Real Time Events

All important state changes use WebSocket events:

```text
heartbeat
agent_update
alert
queue_snapshot
311_surge
cascade_start
cascade_node
cascade_complete
simulation_reset
reroute_update
cv_update
cv_status
```

## REST Endpoints

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

## Design Rules

Core Catalyst followed these project rules:

* No real secrets in GitHub
* CSS variables for theme colors
* Dark and light theme support
* WebSocket updates for real time data
* No frontend backend coupling beyond environment variables
* No provider restructuring after Phase 0

## Current Completion

The planned phases are complete through Phase 6. The project is ready for local demo testing. Deployment remains a separate final step because hosted YOLO inference can require more memory than a small free container provides.
