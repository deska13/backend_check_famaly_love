from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean, ARRAY
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmMBTIQuiz(BaseOrmModel):
    __tablename__ = "mbti_quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    compatibility_quiz_id = Column(Integer, ForeignKey(
        "compatibility_quiz.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(),
                        nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )

    is_male = Column(Boolean)
    first_organizing = Column(ARRAY(Integer))
    first_communicability = Column(ARRAY(Integer))
    first_practicality = Column(ARRAY(Integer))
    first_logicality = Column(ARRAY(Integer))

    second_organizing = Column(ARRAY(Integer))
    second_communicability = Column(ARRAY(Integer))
    second_practicality = Column(ARRAY(Integer))
    second_logicality = Column(ARRAY(Integer))

    result = Column(Text)

    compatibility_quiz = relationship("OrmCompatibilityQuiz")
