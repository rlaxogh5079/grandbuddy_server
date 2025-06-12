from model.review import Review
from database.connection import DBObject
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional

class ReviewRepository:

    @staticmethod
    async def create_review(review: Review) -> None:
        async for session in DBObject.get_db():
            session.add(review)
            await session.commit()

    @staticmethod
    async def get_review_by_request_uuid(request_uuid: str) -> Optional[Review]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Review).where(Review.request_uuid == request_uuid)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_review(review_uuid: str) -> None:
        async for session in DBObject.get_db():
            await session.execute(
                delete(Review).where(Review.review_uuid == review_uuid)
            )
            await session.commit()

    @staticmethod
    async def update_review(review_uuid: str, rating: float, content: str | None) -> None:
        async for session in DBObject.get_db():
            await session.execute(
                update(Review)
                .where(Review.review_uuid == review_uuid)
                .values(rating=rating, content=content)
            )
            await session.commit()