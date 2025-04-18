from database.connection import DBObject
from sqlalchemy.future import select
from model.reward import Reward
from typing import List

class RewardRepository:

    @staticmethod
    async def create_reward(reward: Reward) -> None:
        async for session in DBObject.get_db():
            session.add(reward)
            await session.flush()

    @staticmethod
    async def get_rewards_by_youth_uuid(youth_uuid: str) -> List[Reward]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Reward).where(Reward.youth_uuid == youth_uuid)
            )
            return result.scalars().all()
