from typing import Optional, List
from ._base import BaseAPIModel


class FamalyLoveImages(BaseAPIModel):
    male_images: Optional[List[str]]
    female_images: Optional[List[str]]
