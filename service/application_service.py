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