from._base import BaseAPIModel
from typing import List


class BusinessFamalyLoveImages(BaseAPIModel):
    male_images: List[str]
    female_images: List[str]
