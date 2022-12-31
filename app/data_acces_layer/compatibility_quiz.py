from .abstract import AbstractDALCompatibilityQuiz
from models.database import OrmCompatibilityQuiz
from functools import lru_cache
from ._engine import _postgres_async_session
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload


class DALCompatibilityQuiz(AbstractDALCompatibilityQuiz):
    async def create(
        self: 'DALCompatibilityQuiz'
    ) -> OrmCompatibilityQuiz:
        pass


    async def get_by_id(
        self: 'DALCompatibilityQuiz'
    ) -> OrmCompatibilityQuiz:
        async with _postgres_async_session() as session:
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


@lru_cache()
def get_DAL_compatibility_quiz() -> DALCompatibilityQuiz:
    return DALCompatibilityQuiz()
