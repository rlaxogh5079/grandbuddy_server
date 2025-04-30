from model.schema.reward import CreateRewardModel
from service.reward_service import RewardService
from model.response import ResponseModel, Detail
from fastapi import APIRouter

reward_controller = APIRouter(prefix="/reward", tags=["reward"])

@reward_controller.post("", name="보상 지급")
async def create_reward(data: CreateRewardModel):
    status_code, result = await RewardService.create_reward(
        data.youth_uuid, data.points, data.description
    )
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="보상 지급 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="보상 지급 성공", reward_uuid=result)

@reward_controller.get("/{youth_uuid}", name="보상 목록 조회")
async def get_rewards_by_youth(youth_uuid: str):
    status_code, result = await RewardService.get_rewards_by_youth(youth_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="보상 조회 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="보상 조회 성공", rewards=result)

@reward_controller.post("/refund/{reward_uuid}", name="보상 환불")
async def refund_reward(reward_uuid: str):
    status_code, result = await RewardService.refund_reward(reward_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="환불 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message=result)