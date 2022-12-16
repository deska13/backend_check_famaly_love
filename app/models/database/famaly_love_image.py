from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmFamalyLoveImage(BaseOrmModel):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, nullable=False)
    famaly_love_quiz_id = Column(Integer, ForeignKey("famaly_love_quiz.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )
    image_path = Column(Text)
    is_male = Column(Boolean)

    client = relationship("OrmClient")
