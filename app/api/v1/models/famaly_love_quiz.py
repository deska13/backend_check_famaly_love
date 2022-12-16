from._base import BaseAPIModel
from enum import Enum
from typing import Optional, List
from .famaly_love_image import FamalyLoveImages
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeas


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
    exchange_ideas: ExchangeIdeas
    economy_sector_male: List[int]
    economy_sector_female: List[int]
    
    images: FamalyLoveImages
    
    is_send_to_email: bool
    is_consent_to_data_processing: bool
    email: Optional[str] = None


class StatusProcessingQuizEnum(Enum):
    OK = 'Данные обработаны'
    PROCESSING = 'В обработке'
    ERROR = 'Произошла ошибка'


class ResultFamalyLoveQuiz(BaseAPIModel):
    status: StatusProcessingQuizEnum
    
    traceback: Optional[str] = None
    is_load_new_image: bool = False
    is_load_new_quiz: bool = False
    description: Optional[str] = None
