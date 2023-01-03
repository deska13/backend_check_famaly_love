from typing import List
from ._base import BaseAPIModel


class MBTIQuiz(BaseAPIModel):
    first_organizing: List[int]
    first_communicability: List[int]
    first_practicality: List[int]
    first_logicality: List[int]
    second_organizing: List[int]
    second_communicability: List[int]
    second_practicality: List[int]
    second_logicality: List[int]
