from._base import BaseAPIModel
from .compatibility_quiz import BusinessCompatibilityQuiz
from datetime import datetime

class BusinessClient(BaseAPIModel):
    id: int
    created_at: datetime
    updated_at: datetime


class BusinessClientDetail(BusinessClient):
    compatibility_quiz: BusinessCompatibilityQuiz
