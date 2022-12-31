from._base import BaseAPIModel
from typing import List, Optional
from datetime import datetime


class BusinessFamalyLoveImages(BaseAPIModel):
    id: int
    famaly_love_quiz_id: int
    created_at: datetime
    updated_at: datetime
    image_path: str
    is_male: bool

    result: Optional[str]
