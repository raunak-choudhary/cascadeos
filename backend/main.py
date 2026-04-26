import asyncio
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import ws as ws_router
from routers import graph as graph_router

app = FastAPI(title="CascadeOS", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router.router)
app.include_router(graph_router.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "env": settings.APP_ENV,
    }


@app.on_event("startup")
async def start_background_agents():
    """Launch all domain agents + orchestrator as background asyncio tasks."""
    from routers.ws import manager
    from agents.water_agent import WaterAgent
    from agents.transit_agent import TransitAgent
    from agents.health_agent import HealthAgent
    from agents.emergency_agent import EmergencyAgent
    from agents.orchestrator import run_orchestrator

    broadcast = manager.broadcast

    agents = [
        WaterAgent(broadcast),
        TransitAgent(broadcast),
        HealthAgent(broadcast),
        EmergencyAgent(broadcast),
    ]

    for agent in agents:
        asyncio.create_task(agent.run())

    asyncio.create_task(run_orchestrator(broadcast))
