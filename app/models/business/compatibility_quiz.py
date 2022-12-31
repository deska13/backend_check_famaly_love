from._base import BaseAPIModel
from datetime import datetime
from typing import Optional
from .famaly_love_quiz import BusinessFamalyLoveQuiz
from .mbti_quiz import BusinessMBTIQuiz
from .smol_quiz import BusinessSMOLQuiz


class BusinessCompatibilityQuiz(BaseAPIModel):
    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime
    result: Optional[str]


class BusinessCompatibilityQuizDetail(BusinessCompatibilityQuiz):
    famaly_love_quiz: BusinessFamalyLoveQuiz
    mbti_quiz_male: BusinessMBTIQuiz
    mbti_quiz_female: BusinessMBTIQuiz
    smol_quiz_male: BusinessSMOLQuiz
    smol_quiz_female: BusinessSMOLQuiz
