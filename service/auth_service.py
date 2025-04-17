from repository.user_repository import UserRepository
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Optional
import jwt
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    async def verify_password(password, plain_password):
        hashed_password = pwd_context.hash(plain_password)
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            (expires_delta or timedelta(
                minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    @staticmethod
    async def authenticate_user(user_id: str, password: str):
        user = await UserRepository.find_user(by="user_id", value=user_id)
        print(type(user))
        if not user or not await AuthService.verify_password(password, user.password):
            return None

        return user