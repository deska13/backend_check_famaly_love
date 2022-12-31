from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean, ARRAY
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmCompatibilityQuiz(BaseOrmModel):
    __tablename__ = "compatibility_quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )

    result = Column(Text)

    client = relationship("OrmClient")
    famaly_love_quiz: relationship('OrmFamalyLoveQuiz')
    mbti_quiz_male: relationship('OrmMBTIQuiz', primaryjoin='and_(is_male==True)')
    mbti_quiz_female: relationship('OrmMBTIQuiz', primaryjoin='and_(is_male==False)')
    smol_quiz_male: relationship('OrmSMOLQuiz', primaryjoin='and_(is_male==True)')
    smol_quiz_female: relationship('OrmSMOLQuiz', primaryjoin='and_(is_male==False)')
