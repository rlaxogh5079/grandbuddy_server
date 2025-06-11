# repository/application_repository.py
from model.application import Application, ApplicationStatus
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
    async def update_application_status(application_uuid: str, status: str):
        async for session in DBObject.get_db():
            try:
                await session.execute(
                    update(Application).where(Application.application_uuid == application_uuid).values(status=status)
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
            app = result.scalras().first()
            if app:
                return app
            
            return []

    @staticmethod
    async def get_applications_by_request(request_uuid: str) -> list[Application]:
        async for session in DBObject.get_db():
            result = await session.execute(
                select(Application).where(Application.request_uuid == request_uuid)
            )
            return result.scalars().all()
        
    @staticmethod
    async def reject_other_applications(request_uuid: str, accepted_youth_uuid: str):
        async for session in DBObject.get_db():
            await session.execute(
                update(Application)
                .where(
                    Application.request_uuid == request_uuid,
                    Application.youth_uuid != accepted_youth_uuid
                )
                .values(status=ApplicationStatus.rejected.value)
            )
            await session.commit()