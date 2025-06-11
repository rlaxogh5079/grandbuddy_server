from repository.application_repository import ApplicationRepository
from model.application import Application, ApplicationStatus
from repository.request_repository import RequestRepository
from model.response import Detail, ResponseStatusCode
from datetime import datetime, timezone, date, time
from model.request import Request, RequestStatus
from typing import List, Tuple


class RequestService:
    @staticmethod
    async def create_request(senior_uuid: str, title: str, description: str | None = None, available_date: date | None = None, available_start_time: time | None = None, available_end_time: time | None = None) -> Tuple[ResponseStatusCode, Request | Detail]:
        try:
            new_request = Request(
                senior_uuid=senior_uuid,
                title=title,
                description=description,
                available_date=available_date,
                available_start_time=available_start_time,
                available_end_time=available_end_time,
            )
            await RequestRepository.create_request(new_request)
            return ResponseStatusCode.CREATED, new_request
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=f"요청 생성 실패: {str(e)}")

    @staticmethod
    async def get_request_by_uuid(request_uuid: str) -> Tuple[ResponseStatusCode, Request | Detail]:
        try:
            req = await RequestRepository.get_request_by_uuid(request_uuid)
            if not req:
                return ResponseStatusCode.NOT_FOUND, Detail(text="해당 요청을 찾을 수 없습니다.")
            return ResponseStatusCode.SUCCESS, req
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=f"요청 조회 실패: {str(e)}")

    @staticmethod
    async def get_requests_by_senior(senior_uuid: str) -> Tuple[ResponseStatusCode, List[Request] | Detail]:
        try:
            requests = await RequestRepository.get_requests_by_senior(senior_uuid)
            return ResponseStatusCode.SUCCESS, requests
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=f"요청 목록 조회 실패: {str(e)}")

    @staticmethod
    async def update_request_status(request_uuid: str, status_value: RequestStatus) -> Tuple[ResponseStatusCode, None | Detail]:
        try:
            await RequestRepository.update_request_status(request_uuid, status_value)
            return ResponseStatusCode.SUCCESS, None
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=f"요청 상태 업데이트 실패: {str(e)}")

    @staticmethod
    async def complete_request(request_uuid: str) -> Tuple[ResponseStatusCode, None | Detail]:
        try:
            now = datetime.now(timezone.utc)
            await RequestRepository.update_request_status(request_uuid, RequestStatus.completed)
            
            # 별도 completed 필드도 업데이트하려면 다음과 같이 Repository에서 메소드 분리 필요
            request = await RequestRepository.get_request_by_uuid(request_uuid)
            if request:
                request.completed = now
                await RequestRepository.create_request(request)  # 이미 존재하므로 업데이트 용도로 사용
            return ResponseStatusCode.SUCCESS, None
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=f"요청 완료 처리 실패: {str(e)}")

    @staticmethod
    async def delete_request(request_uuid: str) -> Tuple[ResponseStatusCode, None | Detail]:
        try:
            await RequestRepository.delete_request(request_uuid)
            return ResponseStatusCode.NO_CONTENT, None
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=f"요청 삭제 실패: {str(e)}")

    @staticmethod
    async def get_pending_requests_for_youth():
        try:
            requests = await RequestRepository.get_pending_requests_for_youth()
            print(requests)
            request_list = [req.get_attributes() for req in requests]
            return ResponseStatusCode.SUCCESS, request_list
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
        
    @staticmethod
    async def view_request_and_increase_views(request_uuid: str):
        request = await RequestRepository.get_request_by_uuid(request_uuid)
        if request:
            request.views += 1
            await RequestRepository.update_request(request)
        return request

    @staticmethod
    async def apply_to_request(request_uuid: str, applicant_uuid: str):
        application = Application(request_uuid=request_uuid, youth_uuid=applicant_uuid)
        await ApplicationRepository.create_application(application)
        request = await RequestRepository.get_request_by_uuid(request_uuid)
        if request:
            request.applications += 1
            await RequestRepository.update_request(request)
        return application

    @staticmethod
    async def accept_application(request_uuid: str, youth_uuid: str):
        application = await ApplicationRepository.get_application_by_uuid(youth_uuid)
        if not application:
            return ResponseStatusCode.NOT_FOUND, Detail(text="신청을 찾을 수 없습니다.")
        await ApplicationRepository.update_application_status(youth_uuid, ApplicationStatus.accepted.value)
        await ApplicationRepository.reject_other_applications(request_uuid, youth_uuid)
        return ResponseStatusCode.SUCCESS, None
    
    @staticmethod
    async def get_requests_by_applicant(youth_uuid: str):
        try:
            applications = await ApplicationRepository.get_application_by_uuid(youth_uuid)
            # 신청한 요청들의 request_uuid 모아서 해당 요청 리스트 조회
            print(applications)
            request_uuids = [app.request_uuid for app in applications]
            requests = []
            for request_uuid in request_uuids:
                req = await RequestRepository.get_request_by_uuid(request_uuid)
                if req:
                    requests.append(req)
            return ResponseStatusCode.SUCCESS, requests
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))