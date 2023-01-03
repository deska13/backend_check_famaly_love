from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALFamalyLoveQuiz, get_DAL_famaly_love_quiz
from data_acces_layer.abstract import AbstractDALFamalyLoveQuiz
from models.business import BusinessFamalyLoveQuiz
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from utils.models.famaly_love_quiz_enum import (
    LeisurePreferencesCoincideEnum,
    EducationLevelEnum,
    HousingEnum,
    ExploreTogetherEnum,
    ExchangeIdeasEnum
)


class FamalyLoveQuizService:
    def __init__(
        self: 'FamalyLoveQuizService',
        database: DALFamalyLoveQuiz
    ) -> None:
        self.database = database

    async def create(
        self: 'FamalyLoveQuizService',
        compatibility_quiz_id: int,
        height_difference: int,
        weight_difference: int,
        age_difference: int,
        alcoholism: bool,
        political_views_difference: bool,
        leisure_preferences_coincide: LeisurePreferencesCoincideEnum,
        education_level: EducationLevelEnum,
        salary_male: int,
        salary_female: int,
        housing: HousingEnum,
        explore_together: ExploreTogetherEnum,
        exchange_ideas: ExchangeIdeasEnum,
        economy_sector_male: List[int],
        economy_sector_female: List[int],
        session: AsyncSession,
    ) -> None:
        famaly_love_quiz = await self.database.create(
            compatibility_quiz_id=compatibility_quiz_id,
            height_difference=height_difference,
            weight_difference=weight_difference,
            age_difference=age_difference,
            alcoholism=alcoholism,
            political_views_difference=political_views_difference,
            leisure_preferences_coincide=leisure_preferences_coincide,
            education_level=education_level,
            salary_male=salary_male,
            salary_female=salary_female,
            housing=housing,
            explore_together=explore_together,
            exchange_ideas=exchange_ideas,
            economy_sector_male=economy_sector_male,
            economy_sector_female=economy_sector_female,
            session=session
        )
        return BusinessFamalyLoveQuiz.from_orm(famaly_love_quiz)


@lru_cache()
def get_famaly_love_quiz(
    database: DALFamalyLoveQuiz = Depends(get_DAL_famaly_love_quiz),
) -> FamalyLoveQuizService:
    return FamalyLoveQuizService(database)
