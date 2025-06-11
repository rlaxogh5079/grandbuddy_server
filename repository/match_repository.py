from model.match import Match, MatchStatus
from database.connection import DBObject
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import Optional
from enum import Enum

class MatchRepository:

    @staticmethod
    async def create_match(match: Match) -> None:
        async for session in DBObject.get_db():
            try:
                session.add(match)
                await session.commit()
        
            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e

    @staticmethod
    async def get_match_by_request_uuid(request_uuid: str) -> Optional[Match]:
        async for session in DBObject.get_db():
            try:
                result = await session.execute(
                    select(Match).where(Match.request_uuid == request_uuid)
                )
                return result.scalar_one_or_none()
            
            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e
            
    @staticmethod
    async def get_match_by_user_uuid(user_uuid: str) -> Optional[list[Match]]:
        async for session in DBObject.get_db():
            try:
                result = await session.execute(
                    select(Match).where(Match.youth_uuid == user_uuid)
                )
                return result.scalars().all()

            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e

    @staticmethod
    async def update_match_status(match_uuid: str, new_status: Enum) -> None:
        async for session in DBObject.get_db():
            try:
                await session.execute(
                    update(Match)
                    .where(Match.match_uuid == match_uuid)
                    .values(status=new_status)
                )
                await session.commit()

            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e

    @staticmethod
    async def delete_match(match_uuid: str) -> None:
        async for session in DBObject.get_db():
            try:
                await session.execute(
                    delete(Match).where(Match.match_uuid == match_uuid)
                )
                await session.commit()

            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e
            
    @staticmethod
    async def search_match(request_uuid: str, youth_uuid: str) -> Optional[Match]:
        async for session in DBObject.get_db():
            try:
                result = await session.execute(
                    select(Match).where(Match.request_uuid == request_uuid and Match.youth_uuid == youth_uuid)
                )
                return result.scalar_one_or_none()
            
            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e
            
    @staticmethod
    async def get_match_by_match_uuid(match_uuid: str) -> Optional[Match]:
        async for session in DBObject.get_db():
            try:
                result = await session.execute(
                    select(Match).where(Match.match_uuid == match_uuid and Match.status == MatchStatus.accepted)
                )
                return result.scalar_one_or_none()
            
            except SQLAlchemyError as e:
                print(f"Error: {e}")
                await session.rollback()
                raise e
    