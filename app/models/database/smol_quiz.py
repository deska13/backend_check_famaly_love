from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean, ARRAY
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmSMOLQuiz(BaseOrmModel):
    __tablename__ = "smol_quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    compatibility_quiz_id = Column(Integer, ForeignKey(
        "compatibility_quiz.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(),
                        nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )

    is_male = Column(Boolean)
    quiz = Column(ARRAY(Boolean))

    result = Column(Text)

    compatibility_quiz = relationship("OrmCompatibilityQuiz")
