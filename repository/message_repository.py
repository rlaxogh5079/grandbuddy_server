from model.message import Message
from database.connection import DBObject
from sqlalchemy.future import select

class MessageRepository:

    @staticmethod
    async def save_message(message: Message):
        async for session in DBObject.get_db():
            session.add(message)
            await session.commit()

    @staticmethod
    async def get_messages_by_match(match_uuid: str):
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Message).where(Message.match_uuid == match_uuid)
            )
            return result.scalars().all()

    @staticmethod
    async def get_last_message_by_match(session, match_uuid: str):
        stmt = (
            select(Message)
            .where(Message.match_uuid == match_uuid)
            .order_by(Message.created.desc())
            .limit(1)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()