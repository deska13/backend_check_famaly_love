from._base import BaseAPIModel
from typing import List


class BlockMBTIQuiz(BaseAPIModel):
    first: List[int]
    second: List[int]


class MBTIQuiz(BaseAPIModel):
    organizing: BlockMBTIQuiz
    communicability: BlockMBTIQuiz
    practicality: BlockMBTIQuiz
    logicality: BlockMBTIQuiz
