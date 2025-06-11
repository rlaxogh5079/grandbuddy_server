from repository.application_repository import ApplicationRepository
from model.application import Application
from model.response import Detail, ResponseStatusCode

class ApplicationService:
    @staticmethod
    async def get_applications_by_request(request_uuid: str):
        try:
            applications = await ApplicationRepository.get_applications_by_request(request_uuid)
            return ResponseStatusCode.SUCCESS, applications
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
    
    @staticmethod
    async def cancel_application(request_uuid: str, youth_uuid: str):
        try:
            # "신청 상태를 canceled"로 변경 or 삭제
            from repository.application_repository import ApplicationRepository
            await ApplicationRepository.cancel_application(request_uuid, youth_uuid)
            return ResponseStatusCode.SUCCESS, None
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))