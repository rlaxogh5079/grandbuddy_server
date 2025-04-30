from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, match_uuid: str, websocket: WebSocket):
        await websocket.accept()
        if match_uuid not in self.active_connections:
            self.active_connections[match_uuid] = []
        self.active_connections[match_uuid].append(websocket)

    def disconnect(self, match_uuid: str, websocket: WebSocket):
        self.active_connections[match_uuid].remove(websocket)
        if not self.active_connections[match_uuid]:
            del self.active_connections[match_uuid]

    async def broadcast(self, match_uuid: str, message: str):
        if match_uuid in self.active_connections:
            for connection in self.active_connections[match_uuid]:
                await connection.send_text(message)

manager = ConnectionManager()
