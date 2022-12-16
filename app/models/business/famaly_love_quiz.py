from._base import BaseAPIModel
from enum import Enum
from typing import Optional, List
from .famaly_love_image import BusinessFamalyLoveImages
from enum import Enum
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeas


class BusinessFamalyLoveQuiz(BaseAPIModel):
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
    exchange_ideas: ExchangeIdeas
    economy_sector_male: List[int]
    economy_sector_female: List[int]
    
    images: BusinessFamalyLoveImages
    
    is_send_to_email: bool
    is_consent_to_data_processing: bool
    email: Optional[str] = None
