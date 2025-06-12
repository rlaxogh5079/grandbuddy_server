from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from model.message import Message
from websocket.chat_manager import manager
from repository.message_repository import MessageRepository
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from model.message import Message
from repository.message_repository import MessageRepository
from database.connection import DBObject  # 세션 종속성
import uuid
from model.response import ResponseModel, ResponseStatusCode

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


@chat_router.get("/message/last/{match_uuid}")
async def get_last_message(match_uuid: str, session: AsyncSession = Depends(DBObject.get_db)):
    try:
        message = await MessageRepository.get_last_message_by_match(session, match_uuid)
        if message:
            return ResponseModel.show_json(
                ResponseStatusCode.SUCCESS,
                message_uuid=message.message_uuid,
                match_uuid=message.match_uuid,
                sender_uuid=message.sender_uuid,
                receiver_uuid=message.receiver_uuid,
                message=message.message,
                created=message.created.isoformat()
            )
        else:
            return ResponseModel.show_json(
                ResponseStatusCode.NOT_FOUND,
                detail="해당 매칭에 메시지가 없습니다."
            )
    except Exception as e:
        return ResponseModel.show_json(
            ResponseStatusCode.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
@chat_router.get("/message/list/{match_uuid}")
async def get_messages(match_uuid: str, session: AsyncSession = Depends(DBObject.get_db)):
    messages = await MessageRepository.get_messages_by_match(session, match_uuid)
    return ResponseModel.show_json(ResponseStatusCode.SUCCESS, messages=[
        {
            "sender_uuid": m.sender_uuid,
            "message": m.message,
            "created": m.created.isoformat()
        } for m in messages
    ])