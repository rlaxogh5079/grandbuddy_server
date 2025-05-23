from repository.request_repository import RequestRepository
from model.response import Detail, ResponseStatusCode
from model.request import Request, RequestStatus
from datetime import datetime, timezone
from typing import List, Tuple


class RequestService:
    @staticmethod
    async def create_request(senior_uuid: str, title: str, description: str | None = None) -> Tuple[ResponseStatusCode, Request | Detail]:
        try:
            new_request = Request(
                senior_uuid=senior_uuid,
                title=title,
                description=description,
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
            request_list = [req.get_attributes() for req in requests]
            return ResponseStatusCode.SUCCESS, request_list
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))