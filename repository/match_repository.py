from model.match import Match
from database.connection import DBObject
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import Optional
from enum import Enum

class MatchRepository:

    @staticmethod
    async def create_match(match: Match) -> None:
        async for session in DBObject.get_db():
            session.add(match)
            await session.flush()

    @staticmethod
    async def get_match_by_request_uuid(request_uuid: str) -> Optional[Match]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Match).where(Match.request_uuid == request_uuid)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update_match_status(match_uuid: str, new_status: Enum) -> None:
        async for session in DBObject.get_db():
            await session.execute(
                update(Match)
                .where(Match.match_uuid == match_uuid)
                .values(status=new_status)
            )
            await session.flush()

    @staticmethod
    async def delete_match(match_uuid: str) -> None:
        async for session in DBObject.get_db():
            await session.execute(
                delete(Match).where(Match.match_uuid == match_uuid)
            )
            await session.flush()
