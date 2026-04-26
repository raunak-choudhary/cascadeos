# CascadeOS

Multi-agent NYC infrastructure cascade prediction system built for a hackathon demo.

CascadeOS models water, transit, health, and emergency infrastructure as a 40-node NetworkX graph. Four AI agents monitor live city signals, a weighted BFS engine predicts cascade impact, Dijkstra computes emergency reroutes, Claude Sonnet generates city briefings, and YOLOv8 processes NYC DOT camera frames for visual anomaly alerts.

## Current Status

- Phase 0: Foundation complete
- Phase 1: Infrastructure graph, map, and system graph complete
- Phase 2: Agent layer, 311 surge detector, alert priority queue complete
- Phase 3: Cascade prediction engine complete
- Phase 4: Dijkstra rerouting and city briefing complete
- Phase 5: Computer vision signal complete
- Phase 6: Demo polish complete

## Quick Start

Backend:

```bash
cd backend
source .venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open:

```text
http://localhost:5173
```

## Environment

Do not commit real `.env` files. Use the examples:

- `backend/.env.example`
- `frontend/.env.example`

Backend requires:

- `ANTHROPIC_API_KEY`
- `NYC_OPEN_DATA_APP_TOKEN`
- `NYC_311_ENDPOINT`
- `NYC_DOT_CAMERA_API_URL`
- `CORS_ORIGINS`
- `MODEL_CHECKPOINT_PATH`
- `YOLO_MODEL_PATH`
- `ENABLE_CV`
- `ENABLE_TGNN`
- `CASCADE_PLAYBACK_SPEED`
- `CV_POLL_INTERVAL`

Frontend requires:

- `VITE_API_URL`
- `VITE_WS_URL`
- `VITE_MAPBOX_TOKEN`

## Demo Script

1. Open the app in dark mode on a large screen.
2. Start on City Map: every point is a real NYC infrastructure node.
3. Point out larger glowing nodes: betweenness centrality identifies critical junctions.
4. Switch to Agents: four domain agents monitor water, transit, health, and emergency operations.
5. Switch to Simulate.
6. Select `34th St Water Main Break`, then trigger the cascade.
7. Let the animation run: map nodes, timeline, and system graph update in real time.
8. Return to City Map and show the reroute: red dashed blocked corridor, green Dijkstra reroute.
9. Click `Generate City Briefing` and show the structured Claude report.
10. Switch to CV Feeds and show live NYC DOT camera frames with YOLO detections and alerts.

## Keyboard Shortcuts

- `T`: toggle theme
- `R`: reset simulation
- `Space`: trigger the default 34th St water-main demo cascade

Shortcuts are disabled while typing in inputs or selects.

## Verification Commands

Backend:

```bash
cd backend
source .venv/bin/activate
python -c "from main import app; print('OK')"
```

Frontend:

```bash
cd frontend
npm run build
```

CV smoke test:

```bash
cd backend
source .venv/bin/activate
python - <<'PY'
import asyncio
from routers.cv import poll_cv_once

async def main():
    results = await poll_cv_once()
    print(len(results), sorted({r["model_status"] for r in results}))

asyncio.run(main())
PY
```

## Deployment Notes

Frontend is designed for Vercel. Set:

- `VITE_API_URL`
- `VITE_WS_URL`
- `VITE_MAPBOX_TOKEN`

Backend is designed for Railway. Set all backend environment variables and make sure the ML dependencies from `backend/requirements-ml.txt` are installed if true YOLO inference is required. Without ML dependencies, the detector code degrades safely, but the demo should run with real YOLO.

For production-like backend start:

```bash
cd backend
source .venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Avoid `--reload` during CV demos if the venv is changing, because file watchers can react to package installs inside `.venv`.

## Architecture

Frontend provider order is intentional and should not be restructured:

```text
ThemeProvider
  AgentProvider
    CascadeProvider
      GraphProvider
        AppShell
```

Core real-time event types:

- `agent_update`
- `alert`
- `queue_snapshot`
- `311_surge`
- `cascade_start`
- `cascade_node`
- `cascade_complete`
- `reroute_update`
- `cv_update`
- `heartbeat`
