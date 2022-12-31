from .abstract import AbstractDALSMOLQuiz
from functools import lru_cache
from models.database import OrmSMOLQuiz
from sqlalchemy import func, select
from ._engine import _postgres_async_session


class DALSMOLQuiz(AbstractDALSMOLQuiz):
    async def create(
        self: 'DALSMOLQuiz'
    ) -> OrmSMOLQuiz:
        pass


    async def get_by_id(
        self: 'DALSMOLQuiz'
    ) -> OrmSMOLQuiz:
        async with _postgres_async_session() as session:
            orm_famaly_love_quiz = await session.execute(
                select(OrmSMOLQuiz)
                .where(OrmSMOLQuiz.id == id)
            )
            return orm_famaly_love_quiz.scalar()


@lru_cache()
def get_DAL_smol_quiz() -> DALSMOLQuiz:
    return DALSMOLQuiz()
