from database.connection import DBObject
from model.task import Task, TaskStatus
from sqlalchemy import update, delete
from sqlalchemy.future import select
from typing import List, Optional

class TaskRepository:

    @staticmethod
    async def create_task(task: Task) -> None:
        async for session in DBObject.get_db():
            session.add(task)
            await session.commit()

    @staticmethod
    async def get_tasks_by_senior(senior_uuid: str) -> List[Task]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Task).where(Task.user_uuid == senior_uuid)
            )
            return result.scalars().all()

    @staticmethod
    async def get_task_by_uuid(task_uuid: str) -> Optional[Task]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Task).where(Task.task_uuid == task_uuid)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update_task(task_uuid: str, updates: dict) -> None:
        async for session in DBObject.get_db():
            await session.execute(
                update(Task)
                .where(Task.task_uuid == task_uuid)
                .values(**updates)
            )
            await session.commit()

    @staticmethod
    async def delete_task(task_uuid: str) -> None:
        async for session in DBObject.get_db():
            await session.execute(delete(Task).where(Task.task_uuid == task_uuid))
            await session.commit()
