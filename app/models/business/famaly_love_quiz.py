from datetime import datetime
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeasEnum
from .famaly_love_image import BusinessFamalyLoveImages
from typing import Optional, List
from enum import Enum
from ._base import BaseAPIModel


class BusinessFamalyLoveQuiz(BaseAPIModel):
    id: int
    compatibility_quiz_id: int
    created_at: datetime
    updated_at: datetime
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


class BusinessFamalyLoveQuizDetail(BusinessFamalyLoveQuiz):
    images: BusinessFamalyLoveImages
