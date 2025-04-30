from repository.reward_repository import RewardRepository
from model.response import ResponseStatusCode, Detail
from model.reward import Reward, RewardStatus
from datetime import datetime, timezone

class RewardService:

    @staticmethod
    async def create_reward(youth_uuid: str, points: int, description: str | None) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            reward = Reward(
                youth_uuid=youth_uuid,
                points=points,
                description=description,
                created=datetime.now(timezone.utc)
            )
            await RewardRepository.create_reward(reward)
            return ResponseStatusCode.CREATED, reward.reward_uuid
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def get_rewards_by_youth(youth_uuid: str) -> tuple[ResponseStatusCode, list[dict] | Detail]:
        try:
            rewards = await RewardRepository.get_rewards_by_youth_uuid(youth_uuid)
            return ResponseStatusCode.OK, [
                {
                    "reward_uuid": reward.reward_uuid,
                    "points": reward.points,
                    "description": reward.description,
                    "created": reward.created,
                }
                for reward in rewards
            ]
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def refund_reward(reward_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            reward = await RewardRepository.get_reward_by_uuid(reward_uuid)
            if not reward:
                return ResponseStatusCode.NOT_FOUND, Detail(text="보상을 찾을 수 없습니다.")
            reward.status = RewardStatus.refunded
            await RewardRepository.update_reward(reward)
            return ResponseStatusCode.OK, "환불 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))