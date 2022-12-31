from._base import BaseAPIModel
from datetime import datetime
from typing import List, Optional


class BusinessSMOLQuiz(BaseAPIModel):
    id: int
    compatibility_quiz_id: int
    created_at: datetime
    updated_at: datetime

    is_male: bool
    quiz: List[bool]

    result: Optional[str]