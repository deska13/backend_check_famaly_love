from .abstract import AbstractDALMBTIQuiz
from models.database import OrmMBTIQuiz
from functools import lru_cache
from ._engine import _postgres_async_session
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload


class DALMBTIQuiz(AbstractDALMBTIQuiz):
    async def create(
        self: 'DALMBTIQuiz'
    ) -> OrmMBTIQuiz:
        pass


    async def get_by_id(
        self: 'DALMBTIQuiz'
    ) -> OrmMBTIQuiz:
        async with _postgres_async_session() as session:
            orm_famaly_love_quiz = await session.execute(
                select(OrmMBTIQuiz)
                .where(OrmMBTIQuiz.id == id)
            )
            return orm_famaly_love_quiz.scalar()


@lru_cache()
def get_DAL_mbti_quiz() -> DALMBTIQuiz:
    return DALMBTIQuiz()
