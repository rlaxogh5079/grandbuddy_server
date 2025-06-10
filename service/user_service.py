from repository.user_repository import UserRepository
from model.response import ResponseStatusCode, Detail
from fastapi.security import OAuth2PasswordBearer
from model.schema.user import CreateUserModel
from service.auth_service import AuthService
from model.auth import TokenModel
from fastapi import Depends
from model.user import User
from typing import Tuple
import traceback
import logging

email_session = {}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


class UserService:
    @staticmethod
    async def login(user_id: str, password: str) -> Tuple[ResponseStatusCode, Detail | TokenModel]:
        try:
            user = await AuthService.authenticate_user(user_id, password)
            if not user:
                return (ResponseStatusCode.NOT_FOUND, Detail(f"'{user_id}'라는 유저 아이디를 가진 유저를 찾을 수 없습니다."))

            access_token = await AuthService.create_access_token(
                data={"sub": user.user_uuid})

            return (ResponseStatusCode.SUCCESS, TokenModel(access_token=access_token, token_type="bearer"))

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    async def signup(user: CreateUserModel) -> Tuple[ResponseStatusCode, Detail | None]:
        try:
            db_user = User(
                user_id=user.user_id,
                password=user.password,
                email=user.email,
                phone=user.phone,
                nickname=user.nickname,
                birthday=user.birthday,
                role=user.role,
                address=user.address,
            )
            
            if await UserRepository.check_exist_user("user_id", db_user.user_id):
                return (ResponseStatusCode.CONFLICT, Detail(f"'{db_user.user_id}'라는 유저 아이디를 가진 유저가 이미 존재합니다."))

            if await UserRepository.check_exist_user("nickname", db_user.nickname):
                return (ResponseStatusCode.CONFLICT, Detail(f"'{db_user.nickname}'라는 닉네임을 가진 유저가 이미 존재합니다."))

            if await UserRepository.check_exist_user("email", db_user.email):
                return (ResponseStatusCode.CONFLICT, Detail(f"'{db_user.email}'라는 이메일을 가진 유저가 이미 존재합니다."))

            await UserRepository.create_user(db_user)
            return (ResponseStatusCode.CREATED, None)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> Tuple[ResponseStatusCode, Detail | User]:
        try:
            user_uuid = TokenModel.decode_token(token)
            if not user_uuid:
                return (ResponseStatusCode.FAIL, Detail(f"'{token}'은 유요한 토큰이 아닙니다."))

            user = await UserRepository.find_user(by="user_uuid", value=user_uuid)
            if not user:
                return (ResponseStatusCode.NOT_FOUND, Detail(f"'{token}'을 할당받은 유저를 찾을 수 없습니다."))

            return (ResponseStatusCode.SUCCESS, user)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))
        
    @staticmethod
    async def get_user(user_uuid: str) -> Tuple[ResponseStatusCode, Detail | User]:
        try:
            user = await UserRepository.find_user(by = "user_uuid", value = user_uuid)
            if not user:
                return (ResponseStatusCode.NOT_FOUND, Detail(f"'{user_uuid}'의 유저를 찾을 수 없습니다."))

            return (ResponseStatusCode.SUCCESS, user)
            
        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))
        

    @staticmethod
    async def update_user(user: User, password: str | None = None, nickname: str | None = None, email: str | None = None, address: str | None = None) -> Tuple[ResponseStatusCode, Detail | User]:
        try:
            user_data = {}

            if password:
                user_data["password"] = password
            if nickname:
                user_data["nickname"] = nickname
            if email:
                user_data["email"] = email
            if address:
                user_data["address"] = address

            await UserRepository.update_user(user, user_data)
            user = await UserRepository.find_user("user_uuid", user.user_uuid)

            return (ResponseStatusCode.SUCCESS, user)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    async def delete_user(user: User, password: str) -> Tuple[ResponseStatusCode, Detail | None]:
        try:
            status_code, result = UserService.login(user.user_id, password)
            if isinstance(result, Detail):
                return (status_code, result)

            UserRepository.delete_user(user)
            return (ResponseStatusCode.SUCCESS, None)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))
