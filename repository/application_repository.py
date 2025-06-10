# repository/application_repository.py
from model.application import Application
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from database.connection import DBObject

class ApplicationRepository:
    @staticmethod
    async def create_application(application: Application):
        async for session in DBObject.get_db():
            try:
                session.add(application)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def get_applications_by_request(request_uuid: str):
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Application).where(Application.request_uuid == request_uuid)
            )
            return result.scalars().all()

    @staticmethod
    async def update_application_status(youth_uuid: str, status: str):
        async for session in DBObject.get_db():
            try:
                await session.execute(
                    update(Application).where(Application.youth_uuid == youth_uuid).values(status=status)
                )
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @staticmethod
    async def get_application_by_uuid(youth_uuid: str):
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Application).where(Application.youth_uuid == youth_uuid)
            )
            return result.scalars().all()

    @staticmethod
    async def get_applications_by_request(request_uuid: str) -> list[Application]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Application).where(Application.request_uuid == request_uuid)
            )
            return result.scalars().all()