from model.schema.match import CreateMatchModel, UpdateMatchStatusModel
from service.match_service import MatchService
from model.response import ResponseModel
from fastapi import APIRouter, Depends
from model.response import Detail

match_controller = APIRouter(prefix="/match", tags=["match"])

@match_controller.post("", name="매칭 생성")
async def create_match(data: CreateMatchModel):
    status_code, result = await MatchService.create_match(data.request_uuid, data.youth_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="매칭 생성 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="매칭 생성 성공", match_uuid=result)

@match_controller.delete("/{match_uuid}", name="매칭 삭제")
async def delete_match(match_uuid: str):
    status_code, result = await MatchService.delete_match(match_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="매칭 삭제 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="매칭 삭제 성공")
