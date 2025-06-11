from model.schema.request import CreateRequestModel, UpdateRequestStatusModel
from model.response import ResponseModel, ResponseStatusCode, Detail
from service.request_service import RequestService
from service.match_service import MatchService
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
        description=form_data.description,
        available_date = form_data.available_date,
        available_start_time = form_data.available_start_time,
        available_end_time = form_data.available_end_time
    )
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message = "요청 생성 실패", detail=result.text)

    return ResponseModel.show_json(status_code, message = "요청이 성공적으로 생성되었습니다.", request=result.get_attributes())


@request_controller.get("/{request_uuid}", name="도움 요청 조회(views 카운트 증가)")
async def get_request(
    request_uuid: str = Path(..., description="요청 UUID")
):
    request = await RequestService.view_request_and_increase_views(request_uuid)
    if not request:
        return ResponseModel.show_json(ResponseStatusCode.NOT_FOUND, message="요청 없음")
    return ResponseModel.show_json(ResponseStatusCode.SUCCESS, message="성공 조회", request=request.get_attributes())


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

@request_controller.get("/explore/all", name="청년용 요청 둘러보기")
async def get_pending_requests_for_youth():
    try:
        status_code, result = await RequestService.get_pending_requests_for_youth()
        if isinstance(result, Detail):
            return ResponseModel.show_json(status_code=status_code, message="요청 조회 실패", detail=result.text)
        return ResponseModel.show_json(status_code=status_code, message="요청 조회 성공", requests=result)
    
    except Exception as e:
        print(e)

@request_controller.post("/{request_uuid}/apply", name="신청")
async def apply_to_request(
    request_uuid: str,
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code, message="유저 인증 실패", detail=user.text)
    application = await RequestService.apply_to_request(request_uuid, user.user_uuid)
    return ResponseModel.show_json(ResponseStatusCode.SUCCESS, message="신청 완료", youth_uuid=application.youth_uuid)

@request_controller.post("/{request_uuid}/accept/{youth_uuid}", name="신청 수락")
async def accept_application(
    request_uuid: str,
    youth_uuid: str,
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code, message="유저 인증 실패", detail=user.text)
    # 권한 체크(생략)
    status, result = await RequestService.accept_application(request_uuid, youth_uuid)
    
    if status != ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(status, message="신청 수락 실패", detail=result.text)
    
    await MatchService.create_match(request_uuid, youth_uuid)
    return ResponseModel.show_json(ResponseStatusCode.SUCCESS, message="신청 수락 및 매칭 생성")

@request_controller.get("/applied/me", name="내가 신청한 요청들 조회")
async def get_my_applications(
    current_user: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)
):
    status_code, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status_code, message="유저 인증 실패", detail=user.text)

    status_code, result = await RequestService.get_requests_by_applicant(user.user_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code, message="신청 목록 조회 실패", detail=result.text)
    return ResponseModel.show_json(status_code, message="신청 목록 조회 성공", requests=[r.get_attributes() for r in result])

from service.application_service import ApplicationService

@request_controller.get("/{request_uuid}/applications", name="요청별 신청 목록")
async def get_applications_for_request(
    request_uuid: str,
):
    status, applications = await ApplicationService.get_applications_by_request(request_uuid)
    if status != ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(status, message="신청 목록 조회 실패")
    # 응답 포맷: 신청 리스트
    return ResponseModel.show_json(
        status,
        message="신청 목록",
        applications=[a.get_attributes() for a in applications]
    )
    
@request_controller.delete("/{request_uuid}/application", name="신청 취소")
async def cancel_application(
    request_uuid: str,
    current_user = Depends(UserService.get_current_user)
):
    status, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status, message="유저 인증 실패", detail=user.text)
    # 실제 취소 서비스 호출
    status, detail = await ApplicationService.cancel_application(request_uuid, user.user_uuid)
    if status == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(status, message="신청 취소 완료")
    else:
        return ResponseModel.show_json(status, message="신청 취소 실패", detail=detail.text)