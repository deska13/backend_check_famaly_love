from enum import Enum
from typing import Optional
from .smol_quiz import SMOLQuiz
from .mbti_quiz import MBTIQuiz
from .famaly_love_images import FamalyLoveImages
from .famaly_love_quiz import FamalyLoveQuiz
from ._base import BaseAPIModel
from utils.models import CharacterType, PersonalityType


class CompatibilityQuiz(BaseAPIModel):
    famaly_love_quiz: FamalyLoveQuiz

    mbti_quiz_male: MBTIQuiz
    mbti_quiz_female: MBTIQuiz
    smol_quiz_male: SMOLQuiz
    smol_quiz_female: SMOLQuiz

    images: Optional[FamalyLoveImages]

    is_send_to_email: bool
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

    male_personality_type: Optional[PersonalityType]
    male_personality_desc: str = ''
    male_character_type: Optional[CharacterType]
    male_character_desc: str = ''
    female_personality_type: Optional[PersonalityType]
    female_personality_desc: str = ''
    female_character_type: Optional[CharacterType]
    female_character_desc: str = ''
    years_compatibility_str: Optional[str]
    years_business_str: Optional[str]

    description: Optional[str] = None
