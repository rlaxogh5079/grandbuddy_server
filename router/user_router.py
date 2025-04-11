from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from model.user import UserRole
from service.user_service import UserService
from database.connection import DBObject  # 🔁 변경된 부분

from pydantic import BaseModel, EmailStr

user_router = APIRouter(prefix="/users", tags=["Users"])

# 요청 & 응답 스키마 정의
class UserCreate(BaseModel):
    user_id: str
    password: str
    email: EmailStr
    phone: str
    nickname: str
    birthday: datetime
    role: UserRole
    address: Optional[str] = None
    profile: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    address: Optional[str] = None
    profile: Optional[str] = None

class UserRead(BaseModel):
    user_uuid: str
    user_id: str
    email: EmailStr
    phone: str
    nickname: str
    birthday: datetime
    role: UserRole
    address: Optional[str]
    profile: Optional[str]
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True

@user_router.post("/", response_model=UserRead)
async def create_user(data: UserCreate, db: AsyncSession = Depends(DBObject.get_db)):
    service = UserService(db)
    try:
        user = await service.create_user(**data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

@user_router.get("/", response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(DBObject.get_db)):
    service = UserService(db)
    return await service.get_all_users()

@user_router.get("/{user_uuid}", response_model=UserRead)
async def get_user(user_uuid: str, db: AsyncSession = Depends(DBObject.get_db)):
    service = UserService(db)
    user = await service.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.patch("/{user_uuid}", response_model=UserRead)
async def update_user(user_uuid: str, data: UserUpdate, db: AsyncSession = Depends(DBObject.get_db)):
    service = UserService(db)
    try:
        user = await service.update_user(user_uuid, **data.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uuid: str, db: AsyncSession = Depends(DBObject.get_db)):
    service = UserService(db)
    success = await service.delete_user(user_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
