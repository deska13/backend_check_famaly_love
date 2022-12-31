from._base import BaseAPIModel
from typing import List
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeasEnum


class FamalyLoveQuizId(BaseAPIModel):
    famaly_quiz_id: int


class FamalyLoveQuiz(BaseAPIModel):
    height_difference: int
    weight_difference: int
    age_difference: int
    alcoholism: bool
    political_views_difference: bool
    leisure_preferences_coincide: LeisurePreferencesCoincideEnum
    education_level: EducationLevelEnum
    salary_male: int
    salary_female: int
    housing: HousingEnum
    explore_together: ExploreTogetherEnum
    exchange_ideas: ExchangeIdeasEnum
    economy_sector_male: List[int]
    economy_sector_female: List[int]
