from model.schema.task import CreateTaskModel, UpdateTaskModel
from model.response import ResponseModel, Detail
from service.task_service import TaskService
from service.user_service import UserService
from fastapi import APIRouter, Depends
from model.user import User

task_controller = APIRouter(prefix="/task", tags=["task"])

@task_controller.post("", name="할 일 생성")
async def create_task(data: CreateTaskModel, current_user: User = Depends(UserService.get_current_user)):
    status, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status, message="유저 인증 실패", detail=user.text)
    
    if user.role.name != "senior":
        return ResponseModel.show_json(status_code=400, message="senior만 할 일을 생성할 수 있습니다.")

    status_code, result = await TaskService.create_task(
        user.user_uuid, data.title, data.description, data.dueDate
    )
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="할 일 생성 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="할 일 생성 성공", task=result)

@task_controller.get("/senior/{senior_uuid}", name="senior의 할 일 목록 조회")
async def get_tasks(senior_uuid: str):
    status_code, result = await TaskService.get_tasks_by_senior(senior_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="할 일 조회 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="할 일 목록 조회 성공", tasks=result)

@task_controller.get("/{task_uuid}", name="할 일 상세 조회")
async def get_task_detail(task_uuid: str):
    status_code, result = await TaskService.get_task_detail(task_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="할 일 상세 조회 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="할 일 상세 조회 성공", task=result)

@task_controller.patch("/{task_uuid}", name="할 일 수정")
async def update_task(task_uuid: str, data: UpdateTaskModel, current_user: User = Depends(UserService.get_current_user)):
    status, user = current_user
    if isinstance(user, Detail):
        return ResponseModel.show_json(status, message="유저 인증 실패", detail=user.text)
    
    if user.role.name != "senior":
        return ResponseModel.show_json(status_code=400, message="senior만 할 일을 수정할 수 있습니다.")
    
    updates = data.dict(exclude_unset=True)
    status_code, result = await TaskService.update_task(task_uuid, user.user_uuid, updates)
    
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="할 일 수정 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message=result)

@task_controller.patch("/{task_uuid}/complete", name="할 일 완료 처리")
async def complete_task(task_uuid: str):
    status_code, result = await TaskService.complete_task(task_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="할 일 완료 처리 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message=result)

@task_controller.delete("/{task_uuid}", name="할 일 삭제")
async def delete_task(task_uuid: str):
    status_code, result = await TaskService.delete_task(task_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="할 일 삭제 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message=result)