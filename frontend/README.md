# CascadeOS Frontend

The CascadeOS frontend is a React and Vite application for exploring NYC infrastructure risk in real time. It gives judges and users one visual place to see the city graph, agent activity, cascade simulation, emergency rerouting, generated briefings, and computer vision feeds.

Core Catalyst built the frontend as the demo surface for CascadeOS. It is designed to feel like an operations console, not a marketing site.

## What The Frontend Shows

* City Map with deck.gl and Mapbox
* System Graph with React Flow
* Agent Panel for four AI agents
* Alert Feed with severity ranked signals
* Priority Queue view for the max heap alert queue
* Simulation view with what if controls and cascade timeline
* Reroute overlay with blocked and alternate paths
* City Briefing panel with copy support
* CV Feeds with camera frames and YOLO boxes
* Dark and light themes

## Main Files

```text
frontend/src/
  App.jsx                         Provider wiring and WebSocket dispatch
  components/layout/AppShell.jsx  Main app shell and view routing
  components/map/CityMap.jsx      deck.gl map, cascade, reroute, camera markers
  components/graph/SystemGraph.jsx
  components/agents/AgentPanel.jsx
  components/agents/AlertFeed.jsx
  components/simulation/SimulationView.jsx
  components/ui/CityBriefing.jsx
  components/cv/CVPanel.jsx
  context/AgentContext.jsx
  context/CascadeContext.jsx
  context/GraphContext.jsx
  services/api.js
  theme/theme.css
  styles/global.css
  styles/responsive.css
```

## Requirements

* Node 20 or newer
* npm
* A running CascadeOS backend
* A Mapbox token

## Setup

From the repo root:

```bash
cd frontend
npm install
```

Create the env file:

```bash
cp .env.example .env
```

Fill in:

```text
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_MAPBOX_TOKEN=
```

## Run Locally

```bash
npm run dev -- --host 0.0.0.0
```

Open:

```text
http://localhost:5173
```

## Build

```bash
npm run build
```

The current build may warn about large chunks because Mapbox, deck.gl, and CV UI dependencies are large. That warning does not mean the build failed.

## Frontend Views

City Map:

* Shows all infrastructure nodes and graph edges
* Shows cascade affected nodes by severity
* Shows Dijkstra reroute overlays
* Shows camera markers and anomaly pulses

System Graph:

* Shows the same graph as a node link diagram
* Updates with cascade state
* Lets users inspect node details

Agents:

* Shows water, transit, health, and emergency agents
* Shows reasoning, confidence, and status
* Includes the alert priority queue visualization

Simulate:

* Lets users trigger preset failures
* Shows cascade timeline as events arrive
* Lets users reset the simulation

CV Feeds:

* Shows one to three NYC DOT camera feeds
* Draws detection boxes over frames
* Highlights anomaly states

Alerts:

* Shows severity ranked alerts from agents, CV, and surge detection

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `T` | Toggle dark and light theme |
| `R` | Reset simulation |
| `Space` | Trigger the default 34th Street water main cascade |

Shortcuts are ignored while a user is typing in form controls.

## Theme Rules

The frontend uses CSS custom properties from `theme/theme.css`. Components should use variables such as:

```css
var(--bg-card)
var(--text-primary)
var(--accent-blue)
var(--cascade-critical)
```

New UI should work in both dark and light themes.

## WebSocket Flow

The frontend connects to:

```text
ws://localhost:8000/ws/main
```

Incoming events flow through:

```text
App.jsx
  AgentContext
  CascadeContext
  GraphContext inside AppShell
```

Agent events update the agent panel, alert feed, priority queue, CV feeds, and camera markers. Cascade events update the map, timeline, and system graph.

## Demo Tips

For the smoothest local demo:

1. Start the backend first.
2. Start the frontend second.
3. Open the app in a desktop browser.
4. Use dark mode unless judges ask to see light mode.
5. Trigger the 34th Street preset from the Simulation view.
6. Return to City Map for rerouting and briefing.
7. Use CV Feeds near the end of the demo.

## Deployment

The frontend is ready for Vercel. Set these environment variables in Vercel:

```text
VITE_API_URL=https://your-backend-domain
VITE_WS_URL=wss://your-backend-domain/ws
VITE_MAPBOX_TOKEN=your-public-mapbox-token
```

The backend CORS setting must include the deployed frontend URL.
