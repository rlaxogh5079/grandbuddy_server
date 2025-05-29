from model.review import Review
from repository.review_repository import ReviewRepository
from model.response import ResponseStatusCode, Detail
from datetime import datetime, timezone

class ReviewService:

    @staticmethod
    async def create_review(request_uuid: str, user_uuid: str, rating: float, content: str | None) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            review = Review(
                request_uuid=request_uuid,
                user_uuid=user_uuid,
                rating=rating,
                content=content,
                created=datetime.now(timezone.utc)
            )
            await ReviewRepository.create_review(review)
            return ResponseStatusCode.CREATED, review.review_uuid
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def get_review_by_request(request_uuid: str) -> tuple[ResponseStatusCode, dict | Detail]:
        try:
            review = await ReviewRepository.get_review_by_request_uuid(request_uuid)
            if not review:
                return ResponseStatusCode.NOT_FOUND, Detail(text="리뷰를 찾을 수 없습니다.")
            return ResponseStatusCode.SUCCESS, {
                "review_uuid": review.review_uuid,
                "rating": float(review.rating),
                "content": review.content,
                "created": review.created,
            }
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def delete_review(review_uuid: str) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            await ReviewRepository.delete_review(review_uuid)
            return ResponseStatusCode.SUCCESS, "리뷰 삭제 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))

    @staticmethod
    async def update_review(review_uuid: str, rating: float, content: str | None) -> tuple[ResponseStatusCode, str | Detail]:
        try:
            await ReviewRepository.update_review(review_uuid, rating, content)
            return ResponseStatusCode.SUCCESS, "리뷰 수정 완료"
        except Exception as e:
            return ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(text=str(e))
