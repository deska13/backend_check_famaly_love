from .abstract import AbstractDALSMOLQuiz
from functools import lru_cache
from models.database import OrmSMOLQuiz
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class DALSMOLQuiz(AbstractDALSMOLQuiz):
    async def create(
        self: 'DALSMOLQuiz',
        compatibility_quiz_id: int,
        is_male: bool,
        quiz: List[bool],
        session: AsyncSession
    ) -> OrmSMOLQuiz:
        orm_smol_quiz = OrmSMOLQuiz(
            compatibility_quiz_id=compatibility_quiz_id,
            is_male=is_male,
            quiz=quiz
        )
        session.add(orm_smol_quiz)
        await session.flush()
        await session.refresh(orm_smol_quiz)
        return orm_smol_quiz

    async def get_by_id(
        self: 'DALSMOLQuiz',
        session: AsyncSession
    ) -> OrmSMOLQuiz:
        orm_smol_quiz = await session.execute(
            select(OrmSMOLQuiz)
            .where(OrmSMOLQuiz.id == id)
        )
        return orm_smol_quiz.scalar()


@lru_cache()
def get_DAL_smol_quiz() -> DALSMOLQuiz:
    return DALSMOLQuiz()
