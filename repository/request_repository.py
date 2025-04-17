from model.request import Request, RequestStatus
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from database.connection import DBObject

class RequestRepository:
    @staticmethod
    async def create_request(new_request: Request) -> None:
        async for session in DBObject.get_db():
            try:
                session.add(new_request)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def get_request_by_uuid(request_uuid: str) -> Request | None:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Request).where(Request.request_uuid == request_uuid)
            )
            return result.scalars().first()

    @staticmethod
    async def get_requests_by_senior(senior_uuid: str) -> list[Request]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Request).where(Request.senior_uuid == senior_uuid)
            )
            return result.scalars().all()

    @staticmethod
    async def update_request_status(request_uuid: str, status: RequestStatus) -> None:
        async for session in DBObject.get_db():
            try:
                await session.execute(
                    update(Request).where(Request.request_uuid == request_uuid).values(status=status)
                )
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def delete_request(request_uuid: str) -> None:
        async for session in DBObject.get_db():
            try:
                await session.execute(
                    delete(Request).where(Request.request_uuid == request_uuid)
                )
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
