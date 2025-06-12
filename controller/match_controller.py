from model.schema.match import UpdateMatchStatusModel
from model.response import Detail, ResponseStatusCode
from service.match_service import MatchService
from service.user_service import UserService
from model.response import ResponseModel
from database.connection import DBObject
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model.user import User

match_controller = APIRouter(prefix="/match", tags=["match"])

@match_controller.post("/{request_uuid}", name="매칭 생성")
async def create_match(
    request_uuid: str,
    user_result: tuple[ResponseStatusCode, User] = Depends(UserService.get_current_user),
):
    status_code, result = user_result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "유저 변환 오류", detail=result.text)
    
    user = result
    status_code, result = await MatchService.create_match(request_uuid, user.user_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="매칭 생성 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="매칭 생성 성공", match_uuid=result)

@match_controller.delete("/{match_uuid}", name="매칭 삭제")
async def delete_match(match_uuid: str):
    status_code, result = await MatchService.get_match_by_uuid(match_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="매칭 조회 실패", detail=result.text)
        
    status_code, result = await MatchService.delete_match(result.request_uuid, match_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="매칭 삭제 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="매칭 삭제 성공")

@match_controller.get("", name="매칭 검색")
async def search_match(
    request_uuid: str,
    user_result: tuple[ResponseStatusCode, User] = Depends(UserService.get_current_user)
):
    status_code, result = user_result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 변환 실패", detail = result.text)
    user = result

    status_code, result = await MatchService.search_match(request_uuid, user.user_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 실패", detail = result.text)
    
    if status_code == ResponseStatusCode.NOT_FOUND:
        return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 성공")    
    return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 성공", match = result.get_attributes())

@match_controller.get("/me", name="내가 수락한 요청 조회")
async def get_my_match(
    user_result: tuple[ResponseStatusCode, User] = Depends(UserService.get_current_user)
):
    status_code, result = user_result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "유저 변환 실패", detail = result.text)
    
    user = result
    status_code, result = await MatchService.get_match_by_user(user)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 실패", detail = result.text)
    
    if status_code == ResponseStatusCode.NOT_FOUND:
        return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 성공")    
    return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 성공", matches = list(map(lambda x: x.get_attributes(), result)))


@match_controller.get("/user/{user_uuid}")
async def get_matches_by_user(user_uuid: str):
    status_code, result = await UserService.get_user(user_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "유저를 찾을 수 없습니다.", detail = result.text)
    
    user = result
    status_code, result = await MatchService.get_match_by_user(user)
    if status_code != ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 실패")    
    return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 성공", matches = list(map(lambda x: x.get_attributes(), result)))
    

@match_controller.patch("/complete/{match_uuid}")
async def complete_match(
    match_uuid: str,
    user_result: tuple[ResponseStatusCode, User] = Depends(UserService.get_current_user)
):
    status_code, result = user_result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "유저 변환 실패", detail = result.text)
    
    user = result
    status_code, result = await MatchService.get_match_by_uuid(match_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "매칭 검색 실패", detail = result.text)
    
    match = result

    status_code, result = await MatchService.complete_match(match.request_uuid, match_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code = status_code, messsage = "실패", detail = result.text)
    
    return ResponseModel.show_json(status_code = status_code, message = "성공")