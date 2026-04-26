# CLAUDE.md — CascadeOS
## Multi-Agent Urban Infrastructure Cascade Prediction System

---

## CRITICAL RULES — READ BEFORE WRITING A SINGLE LINE

1. **All secrets and API keys must live exclusively in `.env` files.** Never hardcode any value. Every key, URL, port number, and external endpoint must be an environment variable. The operator should only ever need to edit `.env` to configure the entire system.

2. **Dark and light theme must be implemented from the very first component.** Use CSS custom properties (variables) for every color, shadow, and background value. A theme toggle must be visible and functional from Phase 0. No component is considered done until it works correctly in both themes.

3. **Every component must be responsive from the moment it is written.** Target breakpoints: mobile (375px — latest iPhone), tablet (768px — iPad), desktop (1280px+). Never write a component and "fix responsive later." Responsive is part of done.

4. **Frontend and backend are fully decoupled.** They communicate only via the `VITE_API_URL` environment variable. This enables frontend deployment to Vercel and backend deployment to Railway independently.

5. **Phase order is mandatory.** Do not start Phase N+1 until Phase N passes its exit condition. Each phase produces a working, demo-able artifact.

6. **WebSockets for all real-time data.** Agent activity, alerts, cascade events, and CV signals all flow through WebSocket connections. No polling.

---

## Project Overview

CascadeOS predicts cascading infrastructure failures across New York City in real time. It models NYC's water, transit, health, and emergency systems as an interconnected knowledge graph. Specialized LLM agents monitor each domain. When a failure is detected or simulated, a Weighted BFS cascade propagation engine predicts which downstream systems will be affected and in what order. Emergency rerouting runs Dijkstra on the affected graph. A Computer Vision agent pulls NYC DOT camera frames and feeds anomaly detections as live signals into the agent layer.

**The 3-minute demo story:** Trigger a water main failure at 34th Street. Watch the cascade animate across the NYC map. See which hospitals, subway lines, and emergency routes are predicted to fail and when. Watch Dijkstra suggest a reroute. Read the auto-generated city briefing.

---

## Repository Structure

```
cascadeos/
├── .env                        # Root env — shared config
├── .env.example                # Committed to git — shows all required keys with empty values
├── .gitignore
├── CLAUDE.md                   # This file
│
├── frontend/                   # React + Vite
│   ├── .env                    # Frontend env (VITE_ prefixed)
│   ├── .env.example
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── theme/
│   │   │   ├── ThemeProvider.jsx
│   │   │   ├── theme.css           # All CSS custom properties for both themes
│   │   │   └── useTheme.js
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── AppShell.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── TopBar.jsx
│   │   │   │   └── StatusBar.jsx
│   │   │   ├── map/
│   │   │   │   ├── CityMap.jsx         # deck.gl map container
│   │   │   │   ├── InfrastructureLayer.jsx
│   │   │   │   ├── CascadeLayer.jsx
│   │   │   │   ├── RerouteLayer.jsx
│   │   │   │   └── MapControls.jsx
│   │   │   ├── graph/
│   │   │   │   ├── SystemGraph.jsx     # React Flow graph view
│   │   │   │   ├── NodeDetail.jsx
│   │   │   │   └── GraphControls.jsx
│   │   │   ├── agents/
│   │   │   │   ├── AgentPanel.jsx
│   │   │   │   ├── AgentCard.jsx
│   │   │   │   └── AlertFeed.jsx
│   │   │   ├── simulation/
│   │   │   │   ├── SimulationControls.jsx
│   │   │   │   ├── WhatIfPanel.jsx
│   │   │   │   └── CascadeTimeline.jsx
│   │   │   ├── cv/
│   │   │   │   ├── CVPanel.jsx
│   │   │   │   └── CameraFeed.jsx
│   │   │   └── ui/
│   │   │       ├── ThemeToggle.jsx
│   │   │       ├── SeverityBadge.jsx
│   │   │       ├── PriorityQueue.jsx
│   │   │       └── CityBriefing.jsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.js
│   │   │   ├── useCascade.js
│   │   │   └── useAgents.js
│   │   ├── services/
│   │   │   └── api.js
│   │   └── styles/
│   │       ├── global.css
│   │       └── responsive.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── backend/                    # FastAPI
│   ├── .env                    # Backend env
│   ├── .env.example
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # All env var loading via pydantic-settings
│   ├── routers/
│   │   ├── ws.py               # WebSocket endpoints
│   │   ├── simulation.py       # What-if trigger endpoints
│   │   ├── graph.py            # Infrastructure graph endpoints
│   │   ├── briefing.py         # City briefing generation
│   │   └── cv.py               # Computer vision endpoints
│   ├── agents/
│   │   ├── orchestrator.py     # LangGraph coordinator agent
│   │   ├── transit_agent.py
│   │   ├── water_agent.py
│   │   ├── health_agent.py
│   │   └── emergency_agent.py
│   ├── graph/
│   │   ├── infrastructure_graph.py   # NetworkX graph builder
│   │   ├── betweenness.py            # Centrality algorithms
│   │   ├── cascade_bfs.py            # Weighted BFS propagation
│   │   └── dijkstra_reroute.py       # Emergency rerouting
│   ├── ml/
│   │   ├── temporal_gnn.py           # PyTorch Geometric model
│   │   └── train.py
│   ├── cv/
│   │   ├── camera_client.py          # NYC DOT camera API
│   │   └── yolo_detector.py          # YOLOv8 inference
│   ├── data/
│   │   ├── nyc_open_data.py          # NYC Open Data API client
│   │   └── sliding_window_311.py     # 311 surge detector
│   ├── utils/
│   │   ├── priority_queue.py         # Max heap implementation
│   │   └── alert_scorer.py
│   └── requirements.txt
│
└── docs/
    └── architecture.md
```

---

## Environment Variables

### Frontend (`frontend/.env`)

```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

### Backend (`backend/.env`)

```
# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# NYC Open Data
NYC_OPEN_DATA_APP_TOKEN=your_nyc_open_data_token_here
NYC_311_ENDPOINT=https://data.cityofnewyork.us/resource/erm2-nwe9.json

# NYC DOT Camera — fully public, no key required
NYC_DOT_CAMERA_API_URL=https://webcams.nyctmc.org/api/cameras

# Server
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,https://your-vercel-app.vercel.app

# ML
MODEL_CHECKPOINT_PATH=./ml/checkpoints/tgnn_latest.pt
YOLO_MODEL_PATH=./cv/models/yolov8n.pt

# Feature Flags (set to "true" or "false")
ENABLE_CV=true
ENABLE_TGNN=true
```

**Rule:** `backend/config.py` must load every variable above using `pydantic-settings`. If a required variable is missing at startup, the app must crash immediately with a clear error message naming the missing variable. No silent failures.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Frontend framework | React + Vite | React 18 |
| Map rendering | deck.gl | Latest |
| Graph visualization | React Flow | Latest |
| Styling | CSS custom properties + CSS modules | — |
| Agent orchestration | LangGraph | Latest |
| LLM | Claude Sonnet (claude-sonnet-4-20250514) | — |
| Graph algorithms | NetworkX | 3.x |
| ML framework | PyTorch Geometric | Latest |
| Computer Vision | YOLOv8 (ultralytics) | Latest |
| Backend framework | FastAPI | Latest |
| Real-time | WebSockets (native FastAPI) | — |
| Data source | NYC Open Data APIs | — |
| Deployment | Frontend: Vercel / Backend: Railway | — |

---

## Design System

### Color Palette

```css
/* theme.css — loaded globally, never override inline */

:root[data-theme="dark"] {
  --bg-primary: #0a0e1a;
  --bg-secondary: #111827;
  --bg-card: #1a2235;
  --bg-card-hover: #1e2d45;
  --border: #1e3a5f;
  --border-subtle: #162032;

  --text-primary: #e8f4fd;
  --text-secondary: #7fa8c9;
  --text-muted: #4a7090;

  --accent-blue: #00d4ff;
  --accent-orange: #ff6b35;
  --accent-red: #ff3366;
  --accent-green: #00ff9f;
  --accent-yellow: #ffd700;

  --cascade-low: #00ff9f;
  --cascade-medium: #ffd700;
  --cascade-high: #ff6b35;
  --cascade-critical: #ff3366;

  --agent-transit: #ff6b35;
  --agent-water: #00d4ff;
  --agent-health: #ff3366;
  --agent-emergency: #00ff9f;

  --shadow-card: 0 4px 24px rgba(0, 212, 255, 0.08);
  --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.2);
  --glow-red: 0 0 20px rgba(255, 51, 102, 0.4);
}

:root[data-theme="light"] {
  --bg-primary: #f0f6ff;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --bg-card-hover: #f5faff;
  --border: #c8dff0;
  --border-subtle: #e0eef8;

  --text-primary: #0a1628;
  --text-secondary: #2d5a8a;
  --text-muted: #6b9ab8;

  --accent-blue: #0066cc;
  --accent-orange: #d94f1e;
  --accent-red: #cc0033;
  --accent-green: #00803f;
  --accent-yellow: #b38600;

  --cascade-low: #00803f;
  --cascade-medium: #b38600;
  --cascade-high: #d94f1e;
  --cascade-critical: #cc0033;

  --agent-transit: #d94f1e;
  --agent-water: #0066cc;
  --agent-health: #cc0033;
  --agent-emergency: #00803f;

  --shadow-card: 0 4px 24px rgba(0, 102, 204, 0.08);
  --shadow-glow: 0 0 20px rgba(0, 102, 204, 0.12);
  --glow-red: 0 0 20px rgba(204, 0, 51, 0.2);
}
```

### Typography

Use `IBM Plex Mono` for data values, timestamps, and node IDs. Use `DM Sans` for all UI labels and body text. Both loaded from Google Fonts. Never use Inter, Roboto, or system fonts.

### Responsive Breakpoints

```css
/* responsive.css */
/* Mobile first. Always. */

/* Base styles target 375px (iPhone 15) */
/* Tablet: 768px (iPad) */
@media (min-width: 768px) { }

/* Desktop: 1280px */
@media (min-width: 1280px) { }

/* Large: 1920px */
@media (min-width: 1920px) { }
```

### Layout on Mobile
- Map takes full screen
- Bottom sheet slides up for agent panel and alerts
- Theme toggle and status bar stay pinned at top
- React Flow graph view accessible via tab switch
- Simulation controls accessible via floating action button

---

## Phase 0 — Foundation
**Goal:** Everything boots. Theme works. Responsive shell exists. All connections verified.

### Backend Tasks
- [ ] `backend/` initialized with FastAPI
- [ ] `config.py` loads all env vars via pydantic-settings, fails loudly if missing
- [ ] `GET /health` returns `{ status: ok, timestamp, env: development }`
- [ ] WebSocket endpoint at `ws://localhost:8000/ws/main` accepts connections and echoes a heartbeat every 5 seconds
- [ ] CORS configured from `CORS_ORIGINS` env var
- [ ] `requirements.txt` complete

### Frontend Tasks
- [ ] React + Vite initialized
- [ ] `ThemeProvider.jsx` wraps entire app, reads/writes `data-theme` attribute on `<html>`
- [ ] Theme preference persisted to `localStorage`
- [ ] `theme.css` loaded globally with all CSS variables for both themes
- [ ] `ThemeToggle.jsx` component renders sun/moon icon, switches theme on click
- [ ] `AppShell.jsx` renders: TopBar (with theme toggle), Sidebar (collapsible on mobile), main content area
- [ ] Responsive breakpoints working: sidebar collapses on mobile, bottom sheet scaffold ready
- [ ] `useWebSocket.js` hook connects to backend WS, logs heartbeat to console
- [ ] `api.js` service reads `VITE_API_URL` from env, never hardcodes localhost

### Exit Condition
`npm run dev` and `uvicorn main:app --reload` both run without errors. Browser shows the shell. Theme toggle switches between dark and light. WebSocket heartbeat appears in console. Health endpoint returns 200.

---

## Phase 1 — Map and Infrastructure Graph
**Goal:** NYC map renders with infrastructure nodes. Betweenness centrality heatmap active. Click a node to see its connections.

### Backend Tasks

#### Infrastructure Graph (`graph/infrastructure_graph.py`)
Build a NetworkX DiGraph with the following node types. Use real NYC coordinates.

**Water nodes (10-15):** Major water mains and pumping stations in Manhattan and Brooklyn. Source coordinates from NYC DEP open data.

**Transit nodes (10-15):** Key subway stations and interchanges (34th St Herald Square, Atlantic Av, Times Square, Grand Central, Penn Station, Union Square, 14th St, 125th St, Borough Hall, Jackson Heights).

**Hospital nodes (8-10):** NYU Langone, Bellevue, Mount Sinai, NewYork-Presbyterian, Kings County, Maimonides, Jamaica Hospital, Lincoln Hospital.

**Emergency nodes (8-10):** FDNY and NYPD hubs across the five boroughs.

Each node must have:
```python
{
  "id": "unique_string_id",
  "type": "water|transit|health|emergency",
  "name": "Human readable name",
  "lat": float,
  "lng": float,
  "capacity": float,        # 0.0 to 1.0 current load
  "status": "normal|warning|critical|failed",
  "connections": ["node_id_1", "node_id_2"]  # cross-domain connections
}
```

Each edge must have:
```python
{
  "weight": float,          # propagation speed — 0.1 (slow) to 1.0 (instant)
  "type": "dependency|proximity|operational",
  "bidirectional": bool
}
```

#### Betweenness Centrality (`graph/betweenness.py`)
- Run `nx.betweenness_centrality(G, weight="weight")` on graph load
- Normalize scores to 0.0 to 1.0
- Return as dict keyed by node ID
- Expose via `GET /graph/nodes` — each node includes its `centrality_score`
- Expose full edge list via `GET /graph/edges`

### Frontend Tasks

#### Map (`components/map/CityMap.jsx`)
- deck.gl `DeckGL` component over a Mapbox base map
- Map centered on NYC: `[40.7128, -74.0060]`, zoom 11
- `ScatterplotLayer` for infrastructure nodes, color driven by `--agent-{type}` CSS variable colors
- Node radius scales with `centrality_score` — high centrality nodes are visibly larger and glow
- `LineLayer` for graph edges between connected nodes, opacity reflects edge weight
- Click handler on nodes opens `NodeDetail` sidebar panel
- `ArcLayer` for cross-domain connections (water to hospital dependency shown as arcs)

#### System Graph (`components/graph/SystemGraph.jsx`)
- React Flow renders the same NetworkX graph data as a node-edge diagram
- Nodes styled by domain type with matching color system
- Node size reflects centrality score
- Tab toggle in UI switches between "City Map" view and "System Graph" view
- Both views show the same data, different visual representation

#### NodeDetail Sidebar
- Shows on node click: name, type, status, capacity bar, centrality score, connected nodes list
- Each connected node in the list is clickable to jump to that node
- Status shown as colored badge using `--cascade-{level}` CSS variables

### Exit Condition
Map renders with colored nodes. Nodes glow brighter based on centrality. Clicking a node shows its details. System graph tab shows the same network as a React Flow diagram. Both themes work correctly on map and graph.

---

## Phase 2 — Agent Layer
**Goal:** Four LangGraph agents running. 311 sliding window active. Priority queue processing signals. Agent panel shows live reasoning.

### Backend Tasks

#### Priority Queue (`utils/priority_queue.py`)
Implement a max heap priority queue from scratch using Python's `heapq`. Do not use any priority queue library. This is intentional for demonstration of DSA knowledge.

```python
class AlertPriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0  # tiebreaker for equal priority items

    def push(self, alert: dict, priority: float):
        # priority is severity score 0.0 to 10.0
        # higher score = higher priority
        # negate for max heap using heapq (which is min heap by default)

    def pop(self) -> dict:
        # returns highest priority alert

    def peek(self) -> dict:
        # returns without removing

    def size(self) -> int:

    def to_list(self) -> list:
        # returns sorted snapshot for UI display without modifying heap
```

Every alert flowing through the system must pass through this queue. The coordinator agent always pops from this queue to decide what to reason about next.

#### 311 Sliding Window (`data/sliding_window_311.py`)
Implement a sliding window detector using a deque. Fetch 311 complaint data from NYC Open Data every 60 seconds. For each neighborhood (defined by NTA code), maintain a sliding window of complaint counts over the last 10 minutes.

```python
class SlidingWindow311:
    def __init__(self, window_seconds: int = 600, surge_threshold: int = 10):
        # window_seconds: how far back to look
        # surge_threshold: complaints in window that triggers an alert

    def ingest(self, complaints: list[dict]):
        # add new complaints with timestamps to the window
        # evict complaints older than window_seconds

    def detect_surges(self) -> list[dict]:
        # return list of neighborhoods currently in surge
        # each surge includes: nta_code, complaint_count, dominant_complaint_type, severity_score
```

When a surge is detected, create an alert and push it to the `AlertPriorityQueue` with a computed severity score based on complaint volume and type.

#### Agents (`agents/`)

Each domain agent is a LangGraph node. All agents share a common interface:

```python
class BaseAgent:
    domain: str           # "transit" | "water" | "health" | "emergency"
    poll_interval: int    # seconds between data fetches
    
    async def fetch_data(self) -> dict       # pulls from NYC Open Data
    async def analyze(self, data: dict) -> dict  # calls Claude Sonnet
    async def emit_alert(self, alert: dict)  # pushes to priority queue
```

**Transit Agent:** Polls MTA service status API and 311 transit complaints. Detects service disruptions, unusual crowding, and signal failures.

**Water Agent:** Polls NYC DEP water main data and 311 water complaints. Detects pressure anomalies, main breaks, and flooding reports.

**Health Agent:** Polls hospital capacity indicators from NYC Health open data. Detects ER overcapacity, ambulance availability drops.

**Emergency Agent:** Monitors FDNY incident data and NYPD open data feeds. Detects unusual incident clustering by geography.

**Coordinator Agent:** Runs as the orchestrator LangGraph node. Pops alerts from the priority queue, determines if multiple alerts constitute a cascade event, triggers cascade BFS if cascade threshold exceeded (2+ domains affected within 15 minutes), and broadcasts findings via WebSocket.

Each agent must call Claude Sonnet with a system prompt specific to its domain. The LLM output is a structured JSON reasoning block:

```json
{
  "domain": "water",
  "severity": 7.2,
  "signal": "Water main pressure drop detected at 34th St junction",
  "affected_nodes": ["water_34th", "water_herald_sq"],
  "reasoning": "Pressure readings 40% below baseline. Cross-referencing 311 complaints shows 12 water reports in last 8 minutes. High probability of main break.",
  "recommended_action": "Alert Transit and Health agents. Flag 34th St subway entrance nodes.",
  "confidence": 0.87
}
```

#### WebSocket Broadcasting (`routers/ws.py`)
Single WebSocket endpoint at `/ws/main`. Server pushes these event types:

```python
# Event types the server broadcasts:
{
  "type": "agent_update",      # agent reasoning in progress
  "type": "alert",             # new alert pushed to queue
  "type": "cascade_start",     # cascade BFS triggered
  "type": "cascade_node",      # individual node affected by cascade
  "type": "cascade_complete",  # full cascade result
  "type": "queue_snapshot",    # current state of priority queue
  "type": "311_surge",         # 311 sliding window detected surge
  "type": "heartbeat"          # every 5 seconds
}
```

### Frontend Tasks

#### Agent Panel (`components/agents/AgentPanel.jsx`)
- Four `AgentCard` components, one per domain
- Each card shows: domain name, colored status indicator (idle/analyzing/alert), last reasoning text, confidence score, last updated timestamp
- Live reasoning text animates in character by character when a new update arrives (typewriter effect using CSS animation, not JavaScript setInterval)
- Card pulses with `--glow-red` shadow when agent emits a critical alert

#### Alert Feed (`components/agents/AlertFeed.jsx`)
- Scrollable feed of alerts sorted by severity descending
- Each alert shows: domain badge, severity score (color coded by cascade level), signal text, timestamp
- New alerts animate in from the right with a slide-in transition
- Feed accessible as bottom sheet on mobile

#### Priority Queue Visualizer (`components/ui/PriorityQueue.jsx`)
- Shows current contents of the backend priority queue as a visual heap diagram or sorted list
- Updates on every `queue_snapshot` WebSocket event
- Each item shows priority score and domain color
- This is a talking point for technical judges — label it clearly as "Max Heap Alert Queue"

### Exit Condition
All four agent cards are visible and updating. 311 surge detection is running. The alert feed shows live alerts. The priority queue visualizer shows the heap contents updating in real time. Both themes render correctly.

---

## Phase 3 — Cascade Prediction Engine
**Goal:** The money demo. Trigger a failure. Watch it animate. See the timeline.

### Backend Tasks

#### Weighted BFS (`graph/cascade_bfs.py`)
This is the core algorithm. Implement from scratch using Python's `collections.deque`.

```python
def cascade_bfs(
    graph: nx.DiGraph,
    origin_node_id: str,
    failure_time: datetime
) -> list[dict]:
    """
    Runs weighted BFS from origin_node_id across the infrastructure graph.
    Each edge has a 'weight' (propagation speed, 0.1 to 1.0).
    Higher weight = faster propagation = shorter time to impact.
    
    Returns ordered list of cascade events:
    [
        {
            "node_id": str,
            "domain": str,
            "predicted_impact_minutes": float,   # time from failure_time
            "severity": float,                    # 0.0 to 1.0
            "propagation_path": list[str],        # node IDs from origin to this node
            "cascade_depth": int                  # BFS depth level
        }
    ]
    Sorted by predicted_impact_minutes ascending.
    """

    visited = set()
    queue = deque()
    results = []
    
    # Initialize with origin
    queue.append({
        "node_id": origin_node_id,
        "time_minutes": 0.0,
        "path": [origin_node_id],
        "depth": 0
    })
    
    while queue:
        current = queue.popleft()
        node_id = current["node_id"]
        
        if node_id in visited:
            continue
        visited.add(node_id)
        
        # For each neighbor, compute propagation time
        # time = current_time + (1.0 / edge_weight) * base_propagation_minutes
        # base_propagation_minutes = 5.0 for same domain, 12.0 for cross domain
        
        for neighbor in graph.successors(node_id):
            edge_data = graph[node_id][neighbor]
            # compute time and add to queue and results
    
    return sorted(results, key=lambda x: x["predicted_impact_minutes"])
```

Expose via `POST /simulation/trigger`:
```json
{
  "node_id": "water_34th_st",
  "failure_type": "main_break | power_outage | signal_failure | capacity_exceeded"
}
```

Returns full cascade result list and broadcasts each cascade event via WebSocket as `cascade_node` events with a delay matching `predicted_impact_minutes` (use `asyncio.sleep` scaled down for demo purposes — 1 real second per predicted minute, configurable via env var `CASCADE_PLAYBACK_SPEED`).

#### Simulation Router (`routers/simulation.py`)
- `POST /simulation/trigger` — triggers cascade from a given node
- `POST /simulation/reset` — resets all node statuses to normal
- `GET /simulation/scenarios` — returns preset scenarios (34th St water main, Times Square signal failure, Bellevue capacity surge, FDR Drive closure)

### Frontend Tasks

#### What-If Panel (`components/simulation/WhatIfPanel.jsx`)
- Dropdown to select any infrastructure node as failure origin
- Dropdown to select failure type
- "Trigger Cascade" button — large, prominent, slightly ominous in dark mode
- Preset scenario buttons: "34th St Water Main", "Times Square Signal", "Bellevue Surge"
- Reset button to return all nodes to normal

#### Cascade Animation (`components/map/CascadeLayer.jsx`)
On `cascade_start` WebSocket event:
- Origin node pulses red with expanding ring animation (CSS keyframes)
- As each `cascade_node` event arrives:
  - Affected node transitions color to `--cascade-{severity_level}`
  - An animated pulse ring expands from the node
  - A line layer draws the propagation path from origin to affected node
  - Node in React Flow view also updates simultaneously

#### Cascade Timeline (`components/simulation/CascadeTimeline.jsx`)
- Vertical timeline showing each predicted cascade event
- Each item: node name, domain badge, "in X minutes", severity indicator
- Items appear progressively as cascade_node WebSocket events arrive
- On mobile this renders as a horizontal scrollable strip at the bottom

### Exit Condition
Select "34th St Water Main" from presets. Click trigger. Origin node pulses red on the map. Cascade propagates across the map over the next 30 seconds. Timeline fills with predicted failures. React Flow graph shows the same propagation. Reset returns everything to normal. This sequence takes no more than 60 seconds to complete for demo purposes.

---

## Phase 4 — Dijkstra Rerouting and City Briefing
**Goal:** Cascade triggers automatic emergency rerouting. One button generates the city briefing.

### Backend Tasks

#### Dijkstra Rerouting (`graph/dijkstra_reroute.py`)
When a cascade event affects a transit or water node that serves as a routing hub, automatically compute an alternative route.

```python
def find_emergency_reroute(
    graph: nx.DiGraph,
    blocked_nodes: list[str],
    origin: str,
    destination: str
) -> dict:
    """
    Run Dijkstra on the infrastructure graph excluding blocked_nodes.
    Uses NetworkX nx.dijkstra_path with 'weight' as edge attribute.
    
    Returns:
    {
        "original_path": list[str],
        "rerouted_path": list[str],
        "original_cost_minutes": float,
        "rerouted_cost_minutes": float,
        "delay_minutes": float,
        "recommendation": str   # Claude Sonnet generated plain English
    }
    """
```

Trigger rerouting automatically when cascade depth >= 2 and a transit or emergency node is affected.

Expose via `GET /graph/reroute?blocked={node_ids}&from={origin}&to={destination}`

#### City Briefing (`routers/briefing.py`)
`POST /briefing/generate` — collects:
- Current cascade state (all affected nodes, severity scores)
- All active alerts from the queue
- Rerouting recommendations
- Sends to Claude Sonnet with a city official system prompt
- Returns a structured briefing document:

```json
{
  "incident_id": "CASCADE-2024-001",
  "generated_at": "ISO timestamp",
  "severity": "CRITICAL",
  "summary": "string — 2 sentence executive summary",
  "affected_systems": [...],
  "cascade_origin": {...},
  "predicted_peak_impact": "ISO timestamp",
  "recommended_actions": [...],
  "rerouting": {...},
  "full_report": "string — full plain English report"
}
```

### Frontend Tasks

#### Reroute Layer (`components/map/RerouteLayer.jsx`)
- When reroute data arrives via WebSocket:
  - Original blocked route shown as dashed red line on map
  - Suggested reroute shown as solid green line
  - Animated dashes flow along the green line indicating active routing
  - Tooltip on hover shows delay minutes

#### City Briefing UI (`components/ui/CityBriefing.jsx`)
- Floating button in bottom right: "Generate City Briefing"
- On click: shows loading state with "Generating..." animation
- When ready: slides up a full-height panel showing the structured briefing
- Briefing is formatted with clear sections, severity banner at top
- "Copy Report" button copies full text to clipboard
- Panel is scrollable on all screen sizes

### Exit Condition
After triggering a cascade, a reroute line appears on the map. The City Briefing button generates a complete structured report from Claude Sonnet. The report renders cleanly in both themes. Copy button works.

---

## Phase 5 — Computer Vision Signal
**Goal:** At least one live camera feed with YOLO detections feeding into the agent layer.

### Backend Tasks

#### Camera Client (`cv/camera_client.py`)
- Fetch available camera list from NYC DOT API using `NYC_DOT_CAMERA_API_URL` env var
- Prioritize cameras near infrastructure nodes already in the graph
- Download JPEG frames at configurable interval (default 30 seconds, env var `CV_POLL_INTERVAL`)
- Cache last frame per camera

#### YOLO Detector (`cv/yolo_detector.py`)
- Load YOLOv8n model from `YOLO_MODEL_PATH` env var
- Run inference on camera frames
- Detect and score: `congestion`, `stalled_vehicle`, `crowd_density`, `potential_flooding`
- Return detections with bounding boxes and confidence scores:

```python
{
  "camera_id": str,
  "camera_name": str,
  "lat": float,
  "lng": float,
  "frame_timestamp": str,
  "detections": [
    {
      "class": "congestion",
      "confidence": 0.84,
      "bbox": [x1, y1, x2, y2],
      "severity_contribution": 3.2   # score added to priority queue
    }
  ],
  "anomaly_detected": bool,
  "overall_severity": float
}
```

When `anomaly_detected` is True, create an alert and push to priority queue. Alert includes camera location so it can be matched to nearby infrastructure nodes.

Expose via `GET /cv/cameras` and `GET /cv/latest-frame/{camera_id}`.

### Frontend Tasks

#### CV Panel (`components/cv/CVPanel.jsx`)
- Small panel showing 1 to 3 active camera feeds
- Each feed shows latest frame as an `<img>` tag updated on WebSocket event
- Bounding boxes drawn as SVG overlays on top of the image
- Each box color-coded by detection class
- Confidence score shown in corner of each box
- "ANOMALY DETECTED" banner flashes red when an anomaly is active
- Camera location shown as a distinct marker on the city map

#### Map integration
- Camera locations rendered as a distinct icon layer on the deck.gl map
- Cameras with active anomalies pulse with orange ring

### Exit Condition
CV panel shows at least one camera frame updating every 30 seconds. When YOLO detects an anomaly, it appears as an alert in the agent feed and pushes to the priority queue. Camera marker on map pulses when anomaly is active.

---

## Phase 6 — Polish
**Goal:** Demo ready. Everything feels intentional.

- All loading states handled with skeleton screens
- All error states handled with clear messages and retry options
- Smooth transitions between map and graph views (300ms ease)
- Cascade animation timing feels cinematic, not abrupt
- Mobile bottom sheet spring animation
- Keyboard shortcut: `T` to toggle theme, `R` to reset simulation, `Space` to trigger demo scenario
- `README.md` with setup instructions and demo script
- `.env.example` files committed and complete
- All console.log statements removed from production build

---

## Build Status — Updated 2026-04-26

### Phase 0 ✅ — COMPLETE (commit fba2f70)
All exit conditions met. Both servers verified running. Theme toggle works. WebSocket heartbeat confirmed.

### Phase 1 ✅ — COMPLETE (commit 363afce)
All exit conditions met. 40-node NYC graph live. Betweenness centrality computed. deck.gl map renders with glow rings. React Flow system graph renders with geographic layout. NodeDetail panel works in both views. Both themes verified.

### Phase 2 ✅ — COMPLETE (commit f024cd1)
All exit conditions met. Four domain agents live (water, transit, health, emergency). AlertPriorityQueue max-heap built from scratch. SlidingWindow311 deque detector running. Agent cards update in real time via WebSocket with typewriter animation. PriorityQueue visualizer visible in Agent Panel. Both themes verified.

### Phase 3 ✅ — COMPLETE (commit 876e04d + SystemGraph cascade fix)
All exit conditions met. Weighted BFS cascade engine produces 26 events from `water_34th` across water/transit/health domains in ~37 seconds at default playback speed. WhatIfPanel has all 4 preset scenarios + custom trigger. CascadeTimeline animates in as events stream. CityMap shows cascade overlays (origin red, severity-graded affected nodes, propagation path lines). SystemGraph React Flow view simultaneously updates node colors during cascade. Both themes verified.

---

## Architectural Decisions — Deviations from Original Spec

These are intentional design changes made during implementation. Codex must NOT revert them.

### Files that exist under different names than originally planned
| Spec name | Actual file | Reason |
|---|---|---|
| `CascadeLayer.jsx` | Built into `CityMap.jsx` | Cascade overlays share deck.gl layer stack — separating would require lifting all layer state |
| `InfrastructureLayer.jsx` | Built into `CityMap.jsx` | Same reason — all layers in one DeckGL component |
| `SimulationControls.jsx` | `SimulationView.jsx` | WhatIfPanel+CascadeTimeline are inside SimulationView; SimulationView is the composite view |
| `useCascade.js` / `useAgents.js` | `CascadeContext.jsx` / `AgentContext.jsx` | Context API is the correct React pattern; hooks are just wrappers that read context |
| `SeverityBadge.jsx` | CSS classes (`severity--cascade-*`) | Inline badge component was unnecessary — CSS classes cover all severity states |

### Context architecture (do not change)
```
App.jsx
  ThemeProvider
    AgentProvider          ← agent_update, alert, queue_snapshot, 311_surge
      CascadeProvider      ← cascade_start, cascade_node, cascade_complete, simulation_reset
        GraphProvider      ← nodes, edges, selectedNode (wraps AppShell only)
          AppShell
```
All WebSocket messages route through `handleWsMessage` callbacks from each context. Phase 4 should add a `RerouteContext` OR extend `CascadeContext` with reroute state — do NOT add reroute state to `GraphContext`.

### Emergency domain not in cascade path from water_34th
The BFS from `water_34th` hits water/transit/health but NOT emergency nodes. This is because the graph edges from water/transit/health to emergency nodes are proximity-only with low weight. This is realistic (water main breaks don't directly cascade to FDNY dispatch). The demo still covers 3 of 4 domains. If Codex wants emergency in the path, add a `dependency` edge from `health_bellevue` → `emergency_ems_central` in `infrastructure_graph.py`.

---

## Codex Handoff — Phase 4 (Dijkstra Rerouting + City Briefing)

**READ THIS ENTIRE SECTION before writing a single line for Phase 4.**

### Environment setup (same as all prior phases)
```bash
cd /path/to/cascadeos/backend
source .venv/bin/activate   # conda python 3.12.2
# frontend: cd frontend && npm install (already done)
```
**Always use `python` (conda 3.12.2), never `python3` (Homebrew 3.14.2 — wrong).**

### What already exists that Phase 4 builds on

**Backend:**
- `graph/infrastructure_graph.py` — module singleton: `from graph.infrastructure_graph import graph`; access NetworkX DiGraph via `graph.G`
- `routers/simulation.py` — `_node_status: dict[str, str]` holds current runtime node statuses (key=node_id, value=`"failed"|"critical"|"warning"`). Import this for Dijkstra trigger logic.
- `routers/ws.py` — `manager` is the ConnectionManager singleton. Import: `from routers.ws import manager` then `await manager.broadcast({...})`
- `agents/base_agent.py` — `alert_queue` is the shared AlertPriorityQueue instance. Import: `from agents.base_agent import alert_queue`
- `config.py` — `settings` holds all env vars including `ANTHROPIC_API_KEY`

**Frontend:**
- `context/CascadeContext.jsx` — `affectedNodes` (dict nodeId→{severity,status,depth,path,minutes}), `originNodeId`, `cascadeActive`. Add `reroute_update` WS handler here.
- `services/api.js` — `api.generateBriefing()` already wired to `POST /briefing/generate`
- `context/AgentContext.jsx` — `alerts`, `queueSnapshot` available for briefing data
- `App.jsx` — routes all WS messages to `agentHandler(msg)` and `cascadeHandler(msg)`. Add a third handler for reroute events if you add a RerouteContext.

### Phase 4 new files to create

**Backend:**
- `backend/graph/dijkstra_reroute.py` — Dijkstra implementation (see spec below)
- `backend/routers/briefing.py` — City briefing endpoint
- Register both routers in `backend/main.py`

**Frontend:**
- `frontend/src/components/map/RerouteLayer.jsx` — dashed red + solid green line layers on the deck.gl map
- `frontend/src/components/ui/CityBriefing.jsx` — floating button + slide-up briefing panel

### Dijkstra implementation guidance

Use `networkx` — **do not implement from scratch** (unlike BFS which was deliberately from scratch for DSA demo value; Dijkstra is about the UX of rerouting, not the algorithm). Use:
```python
import networkx as nx
# Exclude blocked nodes by working on a subgraph view
available = [n for n in graph.G.nodes if n not in blocked_nodes]
subgraph = graph.G.subgraph(available)
rerouted_path = nx.dijkstra_path(subgraph, source=origin, target=destination, weight='weight')
```
Invert edge weights before Dijkstra: weight 1.0 = fast propagation = should be PREFERRED route (lower cost). Use `cost = 1.0 / edge_weight` when building cost for Dijkstra path length.

The function must return:
```python
{
    "original_path": list[str],        # node IDs
    "rerouted_path": list[str],
    "original_cost_minutes": float,
    "rerouted_cost_minutes": float,
    "delay_minutes": float,
    "recommendation": str,             # Claude Sonnet generated 1-2 sentences
}
```

Auto-trigger rerouting: In `routers/simulation.py`, after broadcasting `cascade_complete`, check if any affected transit or emergency node has depth >= 2. If so, call `find_emergency_reroute` with those nodes as `blocked_nodes` and broadcast the result as `reroute_update` WS event. Default origin/destination: `transit_penn` → `transit_grand_central`.

**Expose via:** `GET /graph/reroute?blocked=node1,node2&from=transit_penn&to=transit_grand_central`

### City Briefing guidance

`POST /briefing/generate` collects:
```python
from routers.simulation import _node_status
from agents.base_agent import alert_queue, agent_states
```
Pass all of this context to Claude Sonnet with this system prompt:
> "You are the Emergency Operations Director for New York City. Generate a structured incident briefing for city officials and emergency responders. Be concise, factual, and actionable."

Return structure:
```json
{
  "incident_id": "CASCADE-YYYYMMDD-HHmm",
  "generated_at": "ISO timestamp",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "summary": "2 sentence executive summary",
  "affected_systems": [{"node_id": ..., "status": ..., "domain": ...}],
  "cascade_origin": {"node_id": ..., "name": ...},
  "predicted_peak_impact": "ISO timestamp (now + 30min if critical)",
  "recommended_actions": ["action 1", "action 2"],
  "rerouting": { ...dijkstra result or null },
  "full_report": "full plain English paragraph"
}
```

### WebSocket message types Phase 4 adds
```
reroute_update   — { original_path, rerouted_path, delay_minutes, recommendation }
```
Briefing is delivered via REST response (not WebSocket). No new WS types needed for briefing.

### Frontend: RerouteLayer.jsx

Add inside `CityMap.jsx`'s layers array (do NOT create a separate DeckGL — everything goes in the same DeckGL):
```jsx
// Listen for reroute state from context, then:
new LineLayer({
  id: 'reroute-blocked',
  data: blockedEdgePairs,
  getColor: [255, 51, 102, 200],
  getDashArray: [6, 4],
  // dashJustified: true (requires PathLayer or TripsLayer for animated dashes)
})
new LineLayer({
  id: 'reroute-path',
  data: reroutedEdgePairs,
  getColor: [0, 255, 159, 220],
  getWidth: 3,
})
```
Animated dashes: use a `TripsLayer` or simply a CSS `stroke-dashoffset` animation via SVG overlay if deck.gl animated dashes are complex. Keep it simple for the demo.

### Frontend: CityBriefing.jsx

Floating button at bottom-right of `app-content`. On click: calls `api.generateBriefing()`, shows spinner, then slides up a full-height overlay panel. Use `position: fixed; bottom: 0; right: 0; width: min(600px, 100vw); height: 80vh` for the panel. Add a "Copy Report" button that calls `navigator.clipboard.writeText(briefing.full_report)`.

### AppShell update for Phase 4
- Add `CityBriefing` button to the map view only (not agents/alerts views)
- `RerouteLayer` renders inside `CityMap.jsx` automatically when reroute state is present

### Installed packages — do not reinstall
| Package | Version |
|---|---|
| deck.gl | 9.3.1 |
| reactflow | 11.11.4 |
| mapbox-gl | 3.22.0 |
| react-map-gl | 8.1.1 |

---

## Codex Tips — General Rules for Phase 4+

1. **Always activate venv first:** `source backend/.venv/bin/activate`
2. **Always test imports before running the server:** `python -c "from main import app; print('OK')"`
3. **Never install ML deps** (`torch`, `ultralytics`, `torch-geometric`, `opencv`) until Phase 5. They are in `backend/requirements-ml.txt`, NOT in the active venv.
4. **BUILD_CHECK:** After any frontend change, run `npm run build` in `frontend/` to catch import errors. A passing build does not guarantee correct behavior — also verify the dev server renders the feature.
5. **CSS variables only** — never use hardcoded colors. Use `var(--accent-blue)`, `var(--cascade-critical)` etc. Both dark and light themes must work.
6. **DO NOT overwrite `.env` files** — real API keys live there. Always `cat` to verify before any file operation touching env files.
7. **CASCADE_PLAYBACK_SPEED** default 1.0 → demo completes in ~37 seconds. If the demo feels slow, set to 2.0 in `backend/.env` (no code change needed). Do NOT change the default.
8. **Commit pattern:** One commit per phase. Stage only the files you changed. Never use `git add -A`.
9. **Push to origin/main** after each phase commit.
10. **graphify** — after each phase, update the knowledge graph: `graphify-out/` contains the prior graph. Run `/graphify . --update` or write a manual semantic chunk (see `graphify-out/.graphify_chunk_01.json` for the format used in Phase 1-3).

### Demo node IDs (do not change these)
| Demo scenario | Node ID |
|---|---|
| Primary demo origin | `water_34th` |
| Times Square trigger | `transit_times_sq` |
| Bellevue surge | `health_bellevue` |
| FDNY depletion | `emergency_fdny_downtown` |
| Default reroute from | `transit_penn` |
| Default reroute to | `transit_grand_central` |

---

## Pre-Hackathon Checklist — Status as of April 25, 2026

### Already Completed — Claude Code must NOT redo these
- [x] GitHub repo created and live: https://github.com/raunak-choudhary/cascadeos
- [x] CLAUDE.md pushed to repo root on `main` branch
- [x] Anthropic API key obtained and stored in `backend/.env`
- [x] NYC Open Data app token obtained and stored in `backend/.env`
- [x] Mapbox public token obtained and stored in `frontend/.env`
- [x] NYC DOT Camera API confirmed fully public — no key needed
- [x] `backend/.env` created with all real keys — 546 bytes, verified
- [x] `frontend/.env` created with all real keys — 110 bytes, verified
- [x] `backend/.env.example` created with empty values — safe to commit
- [x] `frontend/.env.example` created with empty values — safe to commit
- [x] `.gitignore` created at repo root with all correct entries
- [x] YOLOv8 weights downloaded to `backend/cv/models/yolov8n.pt`
- [x] YOLOv8 torchscript downloaded to `backend/cv/models/yolov8n.torchscript`
- [x] Python 3.11+ confirmed on local machine
- [x] Node 20+ confirmed on local machine

### Still Pending — Raunak must complete these manually (browser required)
- [ ] Railway account created — `railway.app` — needed for backend deployment
- [ ] Vercel account connected to GitHub — `vercel.com` — needed for frontend deployment

### What Claude Code handles automatically
- Python venv creation and all pip installs
- Frontend Vite scaffold and all npm installs
- All file and folder creation for every phase
- All git commits and pushes after each phase

---

## Claude Code Bootstrap Instructions

**ALREADY COMPLETED 2026-04-26 — DO NOT RE-RUN ANY OF THESE STEPS.**
The venv exists, requirements are installed, and the frontend scaffold is live. Starting a new session does NOT mean re-running bootstrap. Jump straight to the next pending phase.

### CRITICAL WARNINGS — Read before running anything

- **DO NOT create or overwrite `backend/.env` or `frontend/.env`** — these files already exist with real API keys. Any overwrite destroys the keys and breaks the project.
- **DO NOT create or overwrite `.gitignore`** — it already exists with correct entries. Append only if a new entry is needed.
- **DO NOT re-download YOLOv8 weights** — `backend/cv/models/yolov8n.pt` and `backend/cv/models/yolov8n.torchscript` already exist.
- **DO NOT create the GitHub repo** — it is already live at https://github.com/raunak-choudhary/cascadeos
- **The `backend/` directory already exists** — only create files inside it, do not reinitialize it.

### Step 1 — Verify environment

```bash
python --version   # must be 3.11+
node --version     # must be 20+
npm --version
git remote -v      # must show https://github.com/raunak-choudhary/cascadeos.git
ls backend/.env    # must exist — if missing, STOP and tell the user
ls frontend/.env   # must exist — if missing, STOP and tell the user
ls backend/cv/models/yolov8n.pt  # must exist — if missing, STOP and tell the user
```

If any of the last three checks fail, stop completely and tell the user which file is missing. Do not proceed.

### Step 2 — Create Python virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### Step 3 — Create `backend/requirements.txt` then install

Create this file if it does not exist. If it exists already, do not overwrite — skip to the install command.

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
websockets==13.0
python-multipart==0.0.9
python-dotenv==1.0.1
pydantic-settings==2.4.0
pydantic==2.8.2
anthropic==0.34.2
langchain==0.3.0
langchain-anthropic==0.2.0
langgraph==0.2.16
networkx==3.3
torch==2.4.0
torch-geometric==2.6.0
numpy==1.26.4
scikit-learn==1.5.1
ultralytics==8.2.90
opencv-python-headless==4.10.0.84
Pillow==10.4.0
httpx==0.27.2
aiohttp==3.10.5
python-dateutil==2.9.0
pytz==2024.1
```

```bash
pip install -r requirements.txt
pip freeze > requirements.lock
```

### Step 4 — Scaffold the frontend

The `frontend/` directory does not exist yet. The `frontend/.env` file exists one level up because it was pre-created. Before running the scaffold, temporarily move the `.env` file so Vite does not get confused:

```bash
cd ..
mv frontend/.env /tmp/frontend_env_backup
npm create vite@latest frontend -- --template react
cd frontend
mv /tmp/frontend_env_backup .env
npm install
npm install @deck.gl/core @deck.gl/layers @deck.gl/react @deck.gl/mapbox
npm install reactflow
npm install mapbox-gl
npm install lucide-react
npm install clsx
```

### Step 5 — Verify .env files are intact after scaffold

```bash
cat frontend/.env   # must show VITE_API_URL, VITE_WS_URL, VITE_MAPBOX_TOKEN with real values
cat backend/.env    # must show ANTHROPIC_API_KEY with real value starting with sk-ant-
```

If either file is empty or missing values, stop and tell the user immediately.

### Step 6 — Commit the scaffold

```bash
cd ..
git add .
git commit -m "bootstrap: venv, requirements.txt, frontend scaffold"
git push origin main
```

### Ongoing library rule

Every time Claude Code installs a new Python library it must run `pip freeze > requirements.lock` and add the library to `requirements.txt`. Every npm install auto-updates `package-lock.json` which must be committed. No library is ever left undocumented.

---

## Another Developer Onboarding — Zero Manual Steps

```bash
git clone https://github.com/raunak-choudhary/cascadeos
cd cascadeos/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cd ../frontend
npm install
cp .env.example .env
```


### Pre-downloaded Assets
- [x] YOLOv8n weights already at `backend/cv/models/yolov8n.pt` — do not re-download
- [x] YOLOv8 torchscript already at `backend/cv/models/yolov8n.torchscript` — do not re-download
- [ ] Google Fonts `DM+Sans` and `IBM+Plex+Mono` — Claude Code loads these via Google Fonts CDN link in `index.html`, no manual download needed

### Demo Script Ready
1. Open app in dark mode on a large screen or external monitor
2. Point to the map — "Every node you see is a real NYC infrastructure point"
3. Point to glowing nodes — "These are the most critical. Betweenness centrality tells us which ones, if they fail, break the most other systems"
4. Point to agent panel — "Four AI agents are monitoring each domain right now using live NYC Open Data"
5. Click "34th St Water Main" preset — pause — click "Trigger Cascade"
6. Watch cascade animate — say nothing for 10 seconds, let it land
7. Point to timeline — "We predicted this cascade 37 minutes before the downstream hospitals would have been impacted"
8. Show reroute line — "Dijkstra found the next best emergency vehicle route automatically"
9. Click "Generate City Briefing" — show the Claude-generated report
10. If time: switch to CV panel, show camera feed with detections

---

## Common Failure Points — Know These in Advance

- **deck.gl + React Strict Mode:** deck.gl does not play well with React Strict Mode double-rendering. Disable Strict Mode in `main.jsx` during development.
- **WebSocket reconnection:** The `useWebSocket.js` hook must implement exponential backoff reconnection. Do not assume the WS connection stays alive.
- **NYC Open Data rate limits:** The free tier limits to 1000 requests per rolling 60 minutes without a token. Always include the app token. Always.
- **YOLOv8 on CPU:** Inference will be slow (~2-3 seconds per frame) on CPU. This is fine for a 30-second poll interval. Do not attempt GPU setup during the hackathon.
- **CORS on Railway:** Set `CORS_ORIGINS` env var on Railway to include your Vercel deployment URL before doing the final demo.
- **Mapbox token restrictions:** If using a restricted Mapbox token, whitelist localhost and your Vercel domain before the hackathon starts.
