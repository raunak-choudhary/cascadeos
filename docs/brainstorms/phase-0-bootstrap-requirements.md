---
date: 2026-04-26
topic: phase-0-bootstrap
---

# Phase 0 — Foundation Bootstrap

## Problem Frame

CascadeOS has no running code yet. The repo contains only the CLAUDE.md blueprint, pre-created `.env` files with real keys, and pre-downloaded YOLOv8 weights. Phase 0 must produce a working skeleton: backend boots, frontend boots, theme toggles, WebSocket heartbeat is visible in the console. Nothing else. Every subsequent phase builds on this skeleton.

## Requirements

**Backend**

- R1. FastAPI app initializes at `backend/main.py` with CORS configured from the `CORS_ORIGINS` environment variable.
- R2. A `backend/config.py` module loads all env vars via pydantic-settings. Web/agent/data-layer variables are always required; ML-specific variables (`MODEL_CHECKPOINT_PATH`, `YOLO_MODEL_PATH`) are only validated when their feature flag (`ENABLE_CV`, `ENABLE_TGNN`) is `true`. Any missing required variable causes an immediate startup crash with a clear error naming the missing variable. No silent fallbacks.
- R3. `GET /health` returns `{ status: "ok", timestamp: <ISO>, env: <value of APP_ENV env var, default "development"> }` with a 200 status.
- R4. A WebSocket endpoint at `ws://localhost:8000/ws/main` accepts connections and broadcasts a `{ type: "heartbeat", timestamp: <ISO> }` message every 5 seconds.
- R5. `backend/requirements.txt` covers all web, agent, and data-layer deps at latest stable versions (no pinned version numbers). A `backend/requirements-ml.txt` contains the ML stack (torch, torch-geometric, ultralytics, opencv) and is **not** installed in Phase 0.

**Frontend**

- R6. React + Vite app initializes at `frontend/`. The existing `frontend/.env` file is preserved intact through the scaffold (moved to a temp path during `npm create vite`, then moved back).
- R7. `frontend/src/theme/ThemeProvider.jsx` wraps the entire app, reads and writes the `data-theme` attribute on `<html>`, and persists the user's preference to `localStorage`.
- R8. `frontend/src/theme/theme.css` is loaded globally and contains all CSS custom properties for both `dark` and `light` themes as specified in CLAUDE.md.
- R9. `frontend/src/components/ui/ThemeToggle.jsx` renders a sun/moon icon and switches the active theme on click.
- R10. `frontend/src/components/layout/AppShell.jsx` renders: TopBar (containing the theme toggle), a collapsible Sidebar, and a main content area. On mobile (< 768px), the sidebar is hidden behind a hamburger toggle. A bottom-sheet `<div>` is present in the DOM but empty.
- R11. `frontend/src/hooks/useWebSocket.js` connects to the backend WebSocket URL from `VITE_WS_URL`, logs each heartbeat to the console, and implements exponential backoff reconnection.
- R12. `frontend/src/services/api.js` reads `VITE_API_URL` from the environment for all requests. No hardcoded `localhost` references.
- R13. Google Fonts (`DM Sans` and `IBM Plex Mono`) are loaded via a `<link>` tag in `frontend/index.html`.

**Tooling**

- R14. React Strict Mode is disabled in `frontend/src/main.jsx` (deck.gl double-render incompatibility, added in Phase 1).
- R15. After `pip install -r requirements.txt`, a `backend/requirements.lock` is generated via `pip freeze`.

## Success Criteria

- `uvicorn main:app --reload` runs without errors from `backend/`.
- `npm run dev` runs without errors from `frontend/`.
- The browser shows the AppShell with TopBar and sidebar.
- Clicking the theme toggle visibly switches between dark and light themes.
- The browser console shows a heartbeat message every 5 seconds.
- `GET http://localhost:8000/health` returns 200 with expected JSON.
- `frontend/.env` still contains all three real keys after scaffolding.
- `backend/.env` is unchanged.

## Scope Boundaries

- No map, no graph, no agents, no simulation controls — those are Phase 1+.
- The bottom sheet is DOM-present but empty; no animation or content.
- The sidebar collapse is functional but does not need spring animation (Phase 6 polish).
- The ML stack (`torch`, `torch-geometric`, `ultralytics`) is not installed. Phase 5 installs `requirements-ml.txt`.
- No git commit required as part of Phase 0 exit condition (committed separately).

## Key Decisions

- **Latest stable versions, not pinned:** The CLAUDE.md pinned mid-2024 versions; 18 months of security patches and compatibility fixes outweigh the risk of minor API changes for a hackathon build.
- **Split requirements files:** `requirements.txt` (web + agents) vs `requirements-ml.txt` (ML stack) avoids a 10-minute, 4 GB install in Phase 0 that provides no value until Phase 5.
- **Scaffold-only mobile bottom sheet:** A functional slide-up animation is Phase 6 polish. An empty, correctly-positioned `<div>` is sufficient for Phase 0 and keeps the responsive exit condition testable.
- **Strict Mode disabled from the start:** CLAUDE.md flags deck.gl incompatibility with React Strict Mode. Disabling it now avoids a confusing debugging session in Phase 1.

## Dependencies / Assumptions

- `backend/.env` and `frontend/.env` exist with real keys (pre-verified in checklist).
- `backend/cv/models/yolov8n.pt` and `yolov8n.torchscript` exist and must not be touched.
- Python 3.11+ and Node 20+ are confirmed on the local machine.
- The GitHub remote (`https://github.com/raunak-choudhary/cascadeos.git`) is already set.

## Next Steps

-> `/ce:plan` for structured implementation planning
