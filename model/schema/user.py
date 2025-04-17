from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(Enum):
    senior = 0 # 노인
    youth = 1 # 청년
    

class CreateUserModel(BaseModel):
    user_id: str
    password: str
    nickname: str
    email: str
    phone: str
    birthday: datetime
    role: UserRole
    address: str
    profile: str


class LoginModel(BaseModel):
    user_id: str
    password: str


class ForgotPasswordModel(BaseModel):
    user_id: str
    password: str


class SignoutModel(BaseModel):
    password: str


class UpdateUserModel(BaseModel):
    password: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    profile: Optional[str] = None
    