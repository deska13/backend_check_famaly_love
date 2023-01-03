from .abstract import AbstractDALMBTIQuiz
from models.database import OrmMBTIQuiz
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from typing import List


class DALMBTIQuiz(AbstractDALMBTIQuiz):
    async def create(
        self: 'DALMBTIQuiz',
        compatibility_quiz_id: int,
        is_male: bool,
        first_organizing: List[int],
        first_communicability: List[int],
        first_practicality: List[int],
        first_logicality: List[int],
        second_organizing: List[int],
        second_communicability: List[int],
        second_practicality: List[int],
        second_logicality: List[int],
        session: AsyncSession
    ) -> OrmMBTIQuiz:
        orm_mbti_quiz = OrmMBTIQuiz(
            compatibility_quiz_id=compatibility_quiz_id,
            is_male=is_male,
            first_organizing=first_organizing,
            first_communicability=first_communicability,
            first_practicality=first_practicality,
            first_logicality=first_logicality,
            second_organizing=second_organizing,
            second_communicability=second_communicability,
            second_practicality=second_practicality,
            second_logicality=second_logicality
        )
        session.add(orm_mbti_quiz)
        await session.flush()
        await session.refresh(orm_mbti_quiz)
        return orm_mbti_quiz

    async def get_by_id(
        self: 'DALMBTIQuiz',
        session: AsyncSession
    ) -> OrmMBTIQuiz:
        orm_mbti_quiz = await session.execute(
            select(OrmMBTIQuiz)
            .where(OrmMBTIQuiz.id == id)
        )
        return orm_mbti_quiz.scalar()


@lru_cache()
def get_DAL_mbti_quiz() -> DALMBTIQuiz:
    return DALMBTIQuiz()
