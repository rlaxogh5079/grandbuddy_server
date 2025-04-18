from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from model.message import Message
from websocket.chat_manager import manager
from repository.message_repository import MessageRepository
from datetime import datetime, timezone
import uuid

chat_router = APIRouter()

@chat_router.websocket("/ws/chat/{match_uuid}/{sender_uuid}/{receiver_uuid}")
async def chat(
    websocket: WebSocket, 
    match_uuid: str,
    sender_uuid: str,
    receiver_uuid: str
):
    await manager.connect(match_uuid, websocket)
    try:
        while True:
            data = await websocket.receive_text()

            message_obj = Message(
                message_uuid=str(uuid.uuid4()),
                match_uuid=match_uuid,
                sender_uuid=sender_uuid,
                receiver_uuid=receiver_uuid,
                message=data,
                created=datetime.now(timezone.utc)
            )

            await MessageRepository.save_message(message_obj)
            await manager.broadcast(match_uuid, f"{sender_uuid}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(match_uuid, websocket)
