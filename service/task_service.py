from repository.task_repository import TaskRepository
from model.response import ResponseStatusCode, Detail
from model.task import Task, TaskStatus
from datetime import datetime, timezone
from typing import List

class TaskService:
    @staticmethod
    async def create_task(user_uuid: str, title: str, description: str | None, dueDate: datetime) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            task = Task(
                user_uuid=user_uuid,
                title=title,
                description=description,
                dueDate=dueDate,
                created=datetime.now(timezone.utc)
            )
            await TaskRepository.create_task(task)
            return ResponseStatusCode.CREATED, task
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def get_tasks_by_senior(senior_uuid: str) -> tuple[ResponseStatusCode, List[dict] | Detail]:
        try:
            tasks = await TaskRepository.get_tasks_by_senior(senior_uuid)
            return ResponseStatusCode.SUCCESS, tasks
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def get_task_detail(task_uuid: str) -> tuple[ResponseStatusCode, dict | Detail]:
        try:
            task = await TaskRepository.get_task_by_uuid(task_uuid)
            if not task:
                return ResponseStatusCode.NOT_FOUND, Detail(text="해당 할 일을 찾을 수 없습니다.")
            return ResponseStatusCode.SUCCESS, {
                "task_uuid": task.task_uuid,
                "title": task.title,
                "description": task.description,
                "status": task.status.name,
                "created": task.created,
                "dueDate": task.dueDate,
            }
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def update_task(task_uuid: str, user_uuid: str, updates: dict) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            task = await TaskRepository.get_task_by_uuid(task_uuid)
            if not task:
                return ResponseStatusCode.NOT_FOUND, Detail(text="해당 할 일을 찾을 수 없습니다.")
            if task.user_uuid != user_uuid:
                return ResponseStatusCode.FORBIDDEN, Detail(text="수정 권한이 없습니다.")
            
            if "status" in updates:
                updates["status"] = TaskStatus[updates["status"]]
            await TaskRepository.update_task(task_uuid, updates)
            return ResponseStatusCode.SUCCESS, "할 일 수정 성공"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))