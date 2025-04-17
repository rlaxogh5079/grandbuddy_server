from model.schema.user import CreateUserModel, LoginModel, UpdateUserModel
from model.response import ResponseModel, ResponseStatusCode, Detail
from fastapi.security import OAuth2PasswordRequestForm
from service.user_service import UserService
from fastapi import APIRouter, Depends
from model.user import User
from typing import Tuple

user_controller = APIRouter(
    prefix='/user',
    tags=['user']
)


@user_controller.get("", name="프로필 조회")
async def get_profile(result: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)):
    status_code, result = result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 불러오는데 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저 정보를 성공적으로 불러왔습니다.", user=result.get_attributes())


@user_controller.post("", name="회원가입")
async def signup(user: CreateUserModel):
    status_code, result = await UserService.signup(user)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="회원가입에 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저가 성공적으로 생성되었습니다.")


@user_controller.patch("", name="회원정보 업데이트")
async def update(form_data: UpdateUserModel, result: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)):
    status_code, result = result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 불러오는데 실패하였습니다.", detail=result.text)

    status_code, result = await UserService.update_user(
        result, form_data.password, form_data.nickname, form_data.email, form_data.profile)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 수정하는데 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저 정보를 성공적으로 변경하였습니다.", user=result.get_attributes())


@user_controller.delete("", name="회원탈퇴")
async def signout(password: str, result: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)):
    status_code, result = result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 불러오는데 실패하였습니다.", detail=result.text)

    status_code, result = await UserService.delete_user(result, password)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="회원탈퇴에 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저가 성공적으로 제거되었습니다.")


@user_controller.post("/auth/login", name="로그인")
async def login(form_data: LoginModel):
    status_code, result = await UserService.login(
        form_data.user_id, form_data.password)

    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="아이디 또는 비밀번호가 잘못 입력되었습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="로그인에 성공하였습니다.", token={"access_token": result.access_token, "token_type": result.token_type})


@user_controller.post("/token", name="토큰 발급")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    _, result = await UserService.login(
        form_data.username, form_data.password
    )

    if isinstance(result, Detail):
        return None

    return {"access_token": result.access_token, "token_type": result.token_type}