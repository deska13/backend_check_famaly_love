from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALFamalyLoveQuiz, get_DAL_famaly_love_quiz
from data_acces_layer.abstract import AbstractDALFamalyLoveQuiz
from models.business import BusinessFamalyLoveQuiz


class FamalyLoveQuizService:
    def __init__(
        self: 'FamalyLoveQuizService', 
        database: AbstractDALFamalyLoveQuiz
    ) -> None:
        self.database = database


    async def create(
        self: 'FamalyLoveQuizService',
        
    ) -> None:
        famaly_love_quiz = await self.database.create(
            
        )
        BusinessFamalyLoveQuiz.from_orm(famaly_love_quiz)


@lru_cache()
def get_famaly_love_quiz(
    database: DALFamalyLoveQuiz = Depends(get_DAL_famaly_love_quiz),
) -> FamalyLoveQuizService:
    return FamalyLoveQuizService(database)
