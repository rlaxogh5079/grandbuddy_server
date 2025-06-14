from repository.application_repository import ApplicationRepository
from repository.match_repository import MatchRepository
from model.response import ResponseStatusCode, Detail
from service.request_service import RequestService
from model.match import Match, MatchStatus
from datetime import datetime, timezone
from model.request import RequestStatus
from model.user import User

class MatchService:

    @staticmethod
    async def create_match(request_uuid: str, youth_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            match = Match(
                request_uuid=request_uuid,
                youth_uuid=youth_uuid,
                status=MatchStatus.active,
                created=datetime.now(timezone.utc)
            )
            await MatchRepository.create_match(match)
            await RequestService.update_request_status(request_uuid, status_value = RequestStatus.accepted)
            return ResponseStatusCode.CREATED, match.match_uuid
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def update_match_status(match_uuid: str, status: MatchStatus) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            await MatchRepository.update_match_status(match_uuid, status)
            return ResponseStatusCode.SUCCESS, "상태 업데이트 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def delete_match(match_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            match_object = await MatchRepository.get_match_by_match_uuid(match_uuid)
            await RequestService.update_request_status(match_object.request_uuid, status_value = RequestStatus.pending)
            application = await ApplicationRepository.get_application_by_request_with_match(match_object.request_uuid)
            await MatchRepository.delete_match(match_uuid)
            await ApplicationRepository.delete_application(application.application_uuid)
            return ResponseStatusCode.SUCCESS, "매칭 삭제 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
        
    @staticmethod
    async def get_match_by_user(user: User) -> tuple[ResponseStatusCode, list[Match] | Detail]:
        try:
            result = await MatchRepository.get_match_by_user(user)
            return ResponseStatusCode.SUCCESS, result
        
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
    
    @staticmethod
    async def get_match_by_uuid(match_uuid: str) -> tuple[ResponseStatusCode, Match | Detail]:
        try:
            result = await MatchRepository.get_match_by_match_uuid(match_uuid)
            if result is None:
                return ResponseStatusCode.NOT_FOUND, Detail(text = str("해당 매칭을 찾을 수 없습니다."))
            else:
                return ResponseStatusCode.SUCCESS, result

        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
        
    @staticmethod
    async def complete_match(request_uuid: str, match_uuid: str) -> tuple[ResponseStatusCode, None | Detail]:
        try:
            await MatchRepository.update_match_status(match_uuid, MatchStatus.completed)
            await RequestService.update_request_status(request_uuid, RequestStatus.completed)
            return ResponseStatusCode.SUCCESS, "성공"
        
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
    
    @staticmethod
    async def get_match_by_request_uuid(request_uuid: str) -> tuple[ResponseStatusCode, Match | Detail]:
        try:
            result = await MatchRepository.get_match_by_request_uuid(request_uuid)
            if result is None:
                return ResponseStatusCode.NOT_FOUND, "찾을 수 없음"
            
            return ResponseStatusCode.SUCCESS, result
            
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))