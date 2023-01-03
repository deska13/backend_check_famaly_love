from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALMBTIQuiz, get_DAL_mbti_quiz
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.business import BusinessMBTIQuiz


class MBTIQuizService:
    def __init__(
        self: 'MBTIQuizService',
        database: DALMBTIQuiz
    ) -> None:
        self.database = database

    async def create(
        self: 'MBTIQuizService',
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
    ) -> None:
        mbti_quiz = await self.database.create(
            compatibility_quiz_id=compatibility_quiz_id,
            is_male=is_male,
            first_organizing=first_organizing,
            first_communicability=first_communicability,
            first_practicality=first_practicality,
            first_logicality=first_logicality,
            second_organizing=second_organizing,
            second_communicability=second_communicability,
            second_practicality=second_practicality,
            second_logicality=second_logicality,
            session=session
        )
        return BusinessMBTIQuiz.from_orm(mbti_quiz)


@lru_cache()
def get_mbti_quiz_service(
    database: DALMBTIQuiz = Depends(get_DAL_mbti_quiz)
) -> MBTIQuizService:
    return MBTIQuizService(database)
