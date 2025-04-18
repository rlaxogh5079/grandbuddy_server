from model.schema.review import CreateReviewModel, UpdateReviewModel
from model.response import ResponseModel, Detail
from service.review_service import ReviewService
from fastapi import APIRouter

review_controller = APIRouter(prefix="/review", tags=["review"])

@review_controller.post("", name="리뷰 생성")
async def create_review(data: CreateReviewModel):
    status_code, result = await ReviewService.create_review(
        data.request_uuid, data.user_uuid, data.rating, data.content
    )
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="리뷰 생성 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="리뷰 생성 성공", review_uuid=result)


@review_controller.get("/{request_uuid}", name="요청 리뷰 조회")
async def get_review_by_request(request_uuid: str):
    status_code, result = await ReviewService.get_review_by_request(request_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="리뷰 조회 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="리뷰 조회 성공", review=result)


@review_controller.delete("/{review_uuid}", name="리뷰 삭제")
async def delete_review(review_uuid: str):
    status_code, result = await ReviewService.delete_review(review_uuid)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="리뷰 삭제 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="리뷰 삭제 성공")


@review_controller.patch("/{review_uuid}", name="리뷰 수정")
async def update_review(review_uuid: str, data: UpdateReviewModel):
    status_code, result = await ReviewService.update_review(review_uuid, data.rating, data.content)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="리뷰 수정 실패", detail=result.text)
    return ResponseModel.show_json(status_code=status_code, message="리뷰 수정 성공")
