from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALCompatibilityQuiz, get_DAL_compatibility_quiz
from models.business import BusinessCompatibilityQuiz, BusinessCompatibilityQuizDetail
from models.database import OrmCompatibilityQuiz
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class CompatibilityQuizService:
    def __init__(self: 'CompatibilityQuizService', database: DALCompatibilityQuiz) -> None:
        self.database = database

    async def create(
        self: 'CompatibilityQuizService',
        client_id: int,
        is_send_to_email: bool,
        session: AsyncSession,
        email: Optional[str]
    ) -> BusinessCompatibilityQuiz:
        compatibility_quiz = await self.database.create(
            client_id=client_id,
            is_send_to_email=is_send_to_email,
            email=email,
            session=session
        )
        return BusinessCompatibilityQuiz.from_orm(compatibility_quiz)

    async def get_by_id(
        self: 'CompatibilityQuizService',
        id: int,
        session: AsyncSession
    ) -> BusinessCompatibilityQuizDetail:
        compatibility_quiz = await self.database.get_by_id(id=id, session=session)
        return BusinessCompatibilityQuizDetail.from_orm(compatibility_quiz)

    async def update_by_id(
        self: 'CompatibilityQuizService',
        id: int,
        result: str,
        session: AsyncSession
    ) -> BusinessCompatibilityQuiz:
        compatibility_quiz = await self.database.update_by_id(id=id, result=result, session=session)
        return BusinessCompatibilityQuiz.from_orm(compatibility_quiz)


@lru_cache()
def get_compatibility_quiz_service(
    database: DALCompatibilityQuiz = Depends(get_DAL_compatibility_quiz)
) -> CompatibilityQuizService:
    return CompatibilityQuizService(database)
