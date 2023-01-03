from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALSMOLQuiz, get_DAL_smol_quiz
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.business import BusinessSMOLQuiz


class SMOLQuizService:
    def __init__(
        self: 'SMOLQuizService',
        database: DALSMOLQuiz
    ) -> None:
        self.database = database

    async def create(
        self: 'SMOLQuizService',
        compatibility_quiz_id: int,
        is_male: bool,
        quiz: List[bool],
        session: AsyncSession
    ) -> None:
        smol_quiz = await self.database.create(
            compatibility_quiz_id=compatibility_quiz_id,
            is_male=is_male,
            quiz=quiz,
            session=session
        )
        return BusinessSMOLQuiz.from_orm(smol_quiz)


@lru_cache()
def get_smol_quiz_service(
    database: DALSMOLQuiz = Depends(get_DAL_smol_quiz)
) -> SMOLQuizService:
    return SMOLQuizService(database)
