from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from model.user import User, UserRole
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
        self,
        user_id: str,
        password: str,
        email: str,
        phone: str,
        nickname: str,
        birthday: datetime,
        role: UserRole,
        address: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> User:
        user = User(
            user_id=user_id,
            password=password,
            email=email,
            phone=phone,
            nickname=nickname,
            birthday=birthday,
            role=role,
            address=address,
            profile=profile,
        )
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("중복된 user_id, email 또는 nickname이 존재합니다.")
        return user

    async def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.user_uuid == user_uuid))
        return result.scalar_one_or_none()

    async def get_all_users(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def update_user(
        self,
        user_uuid: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        nickname: Optional[str] = None,
        address: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> Optional[User]:
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return None

        if email:
            user.email = email
        if phone:
            user.phone = phone
        if nickname:
            user.nickname = nickname
        if address:
            user.address = address
        if profile:
            user.profile = profile

        user.updated = datetime.now()

        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("중복된 값이 존재합니다.")
        return user

    async def delete_user(self, user_uuid: str) -> bool:
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True
