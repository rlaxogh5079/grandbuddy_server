from model.match import Match, MatchStatus
from database.connection import DBObject
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, delete
from model.user import User, UserRole
from sqlalchemy.future import select
from model.request import Request
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
    async def get_match_by_user(user: User) -> Optional[list[Match]]:
        async for session in DBObject.get_db():
            try:
                if user.role == UserRole.youth:
                    # 청년은 내가 수락한 매칭만
                    result = await session.execute(
                        select(Match).where(Match.youth_uuid == user.user_uuid)
                    )
                    return result.scalars().all()
                elif user.role == UserRole.senior:
                    # 노인은 내가 만든 요청의 매칭 모두
                    reqs = await session.execute(
                        select(Request.request_uuid).where(Request.senior_uuid == user.user_uuid)
                    )
                    req_uuid_list = [row[0] for row in reqs.fetchall()]
                    if not req_uuid_list:
                        return []
                    result = await session.execute(
                        select(Match).where(Match.request_uuid.in_(req_uuid_list))
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
    