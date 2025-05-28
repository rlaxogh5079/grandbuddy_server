from typing import Literal, Dict, Any, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from database.connection import DBObject
from model.user import User

class UserRepository:
    @staticmethod
    async def find_user(by: Literal["user_uuid", "user_id", "nickname", "email"], value: str) -> Optional[User]:
        async for session in DBObject.get_db():
            stmt = select(User).where(getattr(User, by) == value)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            return user

    @staticmethod
    async def create_user(user: User) -> None:
        async for session in DBObject.get_db():
            session.add(user)
            try:
                await session.commit()
                print(f"'{user.user_uuid}' 유저가 성공적으로 생성되었습니다!")
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def update_user(user: User, user_data: Dict[str, Any]) -> None:
        async for session in DBObject.get_db():
            stmt = update(User).where(User.user_uuid == user.user_uuid).values(**user_data)
            try:
                await session.execute(stmt)
                await session.commit()
                print(f"'{user.user_uuid}'의 정보가 성공적으로 업데이트 되었습니다.")
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def delete_user(user: User) -> None:
        async for session in DBObject.get_db():
            stmt = delete(User).where(User.user_uuid == user.user_uuid)
            try:
                await session.execute(stmt)
                await session.commit()
                print(f"'{user.user_uuid}' 유저가 성공적으로 제거되었습니다!")
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def check_exist_user(by: Literal["user_uuid", "user_id", "nickname", "email"], value: str) -> bool:
        async for session in DBObject.get_db():
            stmt = select(User).where(getattr(User, by) == value)
            result = await session.execute(stmt)
            return result.scalar_one_or_none() is not None
    