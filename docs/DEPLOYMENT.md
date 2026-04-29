# CascadeOS Deployment Guide

This guide explains how a reviewer, recruiter, or future collaborator can deploy CascadeOS after local setup works.

I designed the app as two independent services:

* Backend on Render, Railway, or another Python host
* Frontend on Vercel or another static frontend host

## Local Verification First

Before deployment, verify locally.

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

CV:

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

## Backend Deployment

Recommended host:

```text
Render or Railway
```

Required environment variables:

```text
ANTHROPIC_API_KEY
NYC_OPEN_DATA_APP_TOKEN
NYC_311_ENDPOINT
NYC_DOT_CAMERA_API_URL
HOST
PORT
CORS_ORIGINS
APP_ENV
MODEL_CHECKPOINT_PATH
YOLO_MODEL_PATH
ENABLE_CV
ENABLE_TGNN
CASCADE_PLAYBACK_SPEED
CV_POLL_INTERVAL
```

Suggested production values:

```text
HOST=0.0.0.0
PORT=<platform-provided-port>
APP_ENV=production
NYC_311_ENDPOINT=https://data.cityofnewyork.us/resource/erm2-nwe9.json
NYC_DOT_CAMERA_API_URL=https://webcams.nyctmc.org/api/cameras
CASCADE_PLAYBACK_SPEED=1.0
CV_POLL_INTERVAL=30
```

For platforms that inject their own `PORT`, use the platform value. For local runs, `8000` is fine.

Set `CORS_ORIGINS` to include the deployed frontend URL.

Example:

```text
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

Backend start command:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

## ML Dependencies On Hosted Backend

True YOLO inference needs:

```bash
pip install -r requirements.txt
pip install -r requirements-ml.txt
```

If the platform has memory or build time limits, temporarily set:

```text
ENABLE_CV=false
```

That keeps the rest of CascadeOS usable, but the full Phase 5 computer vision demo will not be active.

If no Temporal GNN checkpoint is deployed, set:

```text
ENABLE_TGNN=false
```

## YOLO Weights

The backend expects:

```text
backend/cv/models/yolov8n.pt
```

Model weights are not committed to GitHub. For deployment, the model must be available through one of these approaches:

* Include the file through the deployment platform storage
* Download it during the build step
* Attach it as a persistent volume

For the hackathon demo, local execution is the most reliable path for YOLO.

## Frontend Deployment

Recommended host:

```text
Vercel
```

Set:

```text
VITE_API_URL=https://your-backend-domain
VITE_WS_URL=wss://your-backend-domain/ws
VITE_MAPBOX_TOKEN=your-mapbox-token
```

Build command:

```bash
npm run build
```

Output directory:

```text
dist
```

## WebSocket Notes

The backend WebSocket endpoint is:

```text
/ws/main
```

If the backend domain is:

```text
https://cascadeos-api.example.com
```

Then the frontend WebSocket env should be:

```text
VITE_WS_URL=wss://cascadeos-api.example.com/ws
```

The frontend hook appends `/main`, so do not include `/main` in the env value.

## Deployment Readiness Checklist

* Backend health route responds.
* Frontend loads without console errors.
* WebSocket status shows connected.
* Mapbox map renders.
* 34th Street cascade can be triggered.
* Reroute appears after cascade completes.
* City briefing returns a structured report.
* CV feeds show frames if ML and model weights are available.
* `CORS_ORIGINS` includes frontend URL.
* `VITE_API_URL` points to backend URL.
* `VITE_WS_URL` uses `wss` in production.

## Honest Deployment Risk

The app is fully ready for local demo. Hosted deployment is likely straightforward for the frontend. The backend is heavier because Phase 5 installs YOLO, torch, torchvision, opencv, and camera polling. A small hosted container may need more memory or a longer build timeout.

For a judge demo, local execution is recommended unless deployment has already been tested end to end.
