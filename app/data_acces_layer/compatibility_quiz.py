from .abstract import AbstractDALCompatibilityQuiz
from models.database import OrmCompatibilityQuiz
from functools import lru_cache
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


class DALCompatibilityQuiz(AbstractDALCompatibilityQuiz):
    async def create(
        self: 'DALCompatibilityQuiz',
        client_id: int,
        is_send_to_email: bool,
        session: AsyncSession,
        email: str = ''
    ) -> OrmCompatibilityQuiz:
        orm_compatibility_quiz = OrmCompatibilityQuiz(
            client_id=client_id,
            is_send_to_email=is_send_to_email,
            email=email
        )
        session.add(orm_compatibility_quiz)
        await session.flush()
        await session.refresh(orm_compatibility_quiz)
        return orm_compatibility_quiz

    async def get_by_id(
        self: 'DALCompatibilityQuiz',
        id: int,
        session: AsyncSession
    ) -> OrmCompatibilityQuiz:
        orm_famaly_love_quiz = await session.execute(
            select(OrmCompatibilityQuiz)
            .options(selectinload(OrmCompatibilityQuiz.famaly_love_quiz))
            .options(selectinload(OrmCompatibilityQuiz.mbti_quiz_male))
            .options(selectinload(OrmCompatibilityQuiz.mbti_quiz_female))
            .options(selectinload(OrmCompatibilityQuiz.smol_quiz_male))
            .options(selectinload(OrmCompatibilityQuiz.smol_quiz_female))
            .where(OrmCompatibilityQuiz.id == id)
        )
        return orm_famaly_love_quiz.scalar()

    async def update_by_id(
        self: 'DALCompatibilityQuiz',
        id: int,
        result: str,
        session: AsyncSession
    ) -> OrmCompatibilityQuiz:
        orm_famaly_love_quiz = await session.execute(
            select(OrmCompatibilityQuiz)
            .where(OrmCompatibilityQuiz.id == id)
        )
        orm_famaly_love_quiz.result = result


@lru_cache()
def get_DAL_compatibility_quiz() -> DALCompatibilityQuiz:
    return DALCompatibilityQuiz()
