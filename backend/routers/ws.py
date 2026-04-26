import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    """Broadcast server — all connected clients receive every event."""

    def __init__(self):
        self._clients: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._clients.append(ws)

    def disconnect(self, ws: WebSocket):
        self._clients.remove(ws)

    async def broadcast(self, payload: dict):
        dead: list[WebSocket] = []
        for ws in self._clients:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            if ws in self._clients:
                self._clients.remove(ws)

    @property
    def client_count(self) -> int:
        return len(self._clients)


# Module-level singleton shared by agents and simulation router
manager = ConnectionManager()


@router.websocket("/ws/main")
async def websocket_main(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(5)
            await manager.broadcast({
                "type": "heartbeat",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "clients": manager.client_count,
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
