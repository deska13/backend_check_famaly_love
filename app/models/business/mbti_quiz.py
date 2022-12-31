from._base import BaseAPIModel
from datetime import datetime
from typing import List, Optional

class BusinessMBTIQuiz(BaseAPIModel):
    id: int
    compatibility_quiz_id: int
    created_at: datetime
    updated_at: datetime

    is_male: bool
    organizing: List[int]
    communicability: List[int]
    practicality: List[int]
    logicality: List[int]

    result: Optional[str]
