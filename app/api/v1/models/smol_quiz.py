from._base import BaseAPIModel
from typing import List

class SMOLQuiz(BaseAPIModel):
    quiz: List[bool]
