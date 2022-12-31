from._base import BaseAPIModel
from .famaly_love_quiz import FamalyLoveQuiz
from .famaly_love_images import FamalyLoveImages
from .mbti_quiz import MBTIQuiz
from .smol_quiz import SMOLQuiz
from typing import Optional
from enum import Enum


class CompatibilityQuiz(BaseAPIModel):
    famaly_love_quiz: FamalyLoveQuiz

    mbti_quiz_male: MBTIQuiz
    mbti_quiz_female: MBTIQuiz
    smol_quiz_male: SMOLQuiz
    smol_quiz_female: SMOLQuiz

    images: FamalyLoveImages
    
    is_send_to_email: bool
    is_consent_to_data_processing: bool
    email: Optional[str] = None


class StatusProcessingCompatibilityQuizEnum(Enum):
    OK = 'Данные обработаны'
    PROCESSING = 'В обработке'
    ERROR = 'Произошла ошибка'


class ResultCompatibilityQuiz(BaseAPIModel):
    status: StatusProcessingCompatibilityQuizEnum
    
    traceback: Optional[str] = None
    is_load_new_image: bool = False
    is_load_new_quiz: bool = False
    description: Optional[str] = None
