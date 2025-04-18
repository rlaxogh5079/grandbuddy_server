from model.schema.request import CreateRequestModel, UpdateRequestStatusModel
from model.response import ResponseModel, ResponseStatusCode, Detail
from service.request_service import RequestService
from service.user_service import UserService
from fastapi import APIRouter, Depends, Path
from model.schema.user import UserRole
from model.user import User
from typing import Tuple

request_controller = APIRouter(prefix="/request", tags=["request"])

# 1. 요청 생성 (senior만 가능)
@request_controller.post("", name="도움 요청 생성")
async def create_request(
    form_data: CreateRequestModel,
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code = status_code, message = "유저 인증 실패", detail=user.text)

    if user.role != UserRole.senior:
        print(user.role, UserRole.senior)
        return ResponseModel.show_json(ResponseStatusCode.FORBIDDEN, message = "요청 생성 권한이 없습니다.")

    status_code, result = await RequestService.create_request(
        senior_uuid=user.user_uuid,
        title=form_data.title,
        description=form_data.description
    )
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message = "요청 생성 실패", detail=result.text)

    return ResponseModel.show_json(status_code, message = "요청이 성공적으로 생성되었습니다.", request=result.get_attributes())

# 2. 요청 단건 조회
@request_controller.get("/{request_uuid}", name="도움 요청 조회")
async def get_request(
    request_uuid: str = Path(..., description="요청 UUID")
):
    status_code, result = await RequestService.get_request_by_uuid(request_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message = "요청 조회 실패", detail=result.text)

    return ResponseModel.show_json(status_code, message = "요청을 성공적으로 불러왔습니다.", request=result.get_attributes())

# 3. senior가 만든 요청들 전체 조회
@request_controller.get("", name="내가 만든 요청들 전체 조회")
async def get_my_requests(
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code, message = "유저 인증 실패", detail=user.text)

    status_code, result = await RequestService.get_requests_by_senior(user.user_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message = "요청 목록 조회 실패", detail=result.text)

    return ResponseModel.show_json(status_code, message = "요청 목록 조회 성공", requests=list(map(lambda x: x.get_attributes(), result)))

# 4. 요청 상태 변경
@request_controller.patch("/{request_uuid}/status", name="요청 상태 변경")
async def update_request_status(
    request_uuid: str,
    form_data: UpdateRequestStatusModel,
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code, message = "유저 인증 실패", detail=user.text)

    status_code, result = await RequestService.update_request_status(request_uuid, form_data.status)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message = "요청 상태 변경 실패", detail=result.text)

    return ResponseModel.show_json(status_code, message = "요청 상태가 성공적으로 변경되었습니다.")

# 5. 요청 삭제
@request_controller.delete("/{request_uuid}", name="요청 삭제")
async def delete_request(
    request_uuid: str,
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code, message = "유저 인증 실패", detail=user.text)

    status_code, result = await RequestService.delete_request(request_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message = "요청 삭제 실패", detail=result.text)

    return ResponseModel.show_json(status_code, message = "요청이 성공적으로 삭제되었습니다.")
