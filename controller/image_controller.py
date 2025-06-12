from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os

from service.user_service import UserService
from model.user import User
from database.connection import DBObject  # DB 세션 함수
from model.response import ResponseModel, ResponseStatusCode
from model.schema.user import UpdateUserModel

image_controller = APIRouter()

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@image_controller.post("/upload-profile-image/")
async def upload_profile_image(
    file: UploadFile = File(...),
    user_result: tuple[ResponseStatusCode, User] = Depends(UserService.get_current_user),
    db: Session = Depends(DBObject.get_db)
):
    status_code, user = user_result

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    filename = f"{user.user_uuid}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await UserService.update_user(user, profile = f"/static/uploads/{filename}")
    await db.commit()

    return ResponseModel.show_json(
        status_code=status_code,
        message="프로필 이미지가 성공적으로 업데이트되었습니다.",
        user=user.get_attributes()
    )


@image_controller.get("/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")

    return FileResponse(file_path, media_type="image/*")
