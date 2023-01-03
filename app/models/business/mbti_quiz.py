from typing import List, Optional
from datetime import datetime
from ._base import BaseAPIModel


class BusinessMBTIQuiz(BaseAPIModel):
    id: int
    compatibility_quiz_id: int
    created_at: datetime
    updated_at: datetime

    is_male: bool
    first_organizing: List[int]
    first_communicability: List[int]
    first_practicality: List[int]
    first_logicality: List[int]
    second_organizing: List[int]
    second_communicability: List[int]
    second_practicality: List[int]
    second_logicality: List[int]

    result: Optional[str]
