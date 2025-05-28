from repository.match_repository import MatchRepository
from model.response import ResponseStatusCode, Detail
from service.request_service import RequestService
from model.match import Match, MatchStatus
from datetime import datetime, timezone
from model.request import RequestStatus

class MatchService:

    @staticmethod
    async def create_match(request_uuid: str, youth_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            match = Match(
                request_uuid=request_uuid,
                youth_uuid=youth_uuid,
                status=MatchStatus.accepted,
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
            return ResponseStatusCode.OK, "상태 업데이트 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def delete_match(match_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            await MatchRepository.delete_match(match_uuid)
            return ResponseStatusCode.OK, "매칭 삭제 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def search_match(request_uuid: str, youth_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            result = await MatchRepository.search_match(request_uuid, youth_uuid)
            if result is None:
                return ResponseStatusCode.NOT_FOUND, Detail(text = str("해당 매칭을 찾을 수 없습니다."))
            else:
                return ResponseStatusCode.SUCCESS, result
            
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))