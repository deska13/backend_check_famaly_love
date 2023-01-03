from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean, ARRAY
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmCompatibilityQuiz(BaseOrmModel):
    __tablename__ = "compatibility_quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey(
        "client.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(),
                        nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )

    is_send_to_email = Column(Boolean)
    is_shipped = Column(Boolean)
    email = Column(Text)

    result = Column(Text)

    client = relationship("OrmClient")
    famaly_love_quiz = relationship(
        'OrmFamalyLoveQuiz',
        uselist=False
    )
    mbti_quiz_male = relationship(
        'OrmMBTIQuiz',
        primaryjoin='and_(OrmCompatibilityQuiz.id==OrmMBTIQuiz.compatibility_quiz_id, OrmMBTIQuiz.is_male==True)',
        uselist=False
    )
    mbti_quiz_female = relationship(
        'OrmMBTIQuiz',
        primaryjoin='and_(OrmCompatibilityQuiz.id==OrmMBTIQuiz.compatibility_quiz_id, OrmMBTIQuiz.is_male==False)',
        uselist=False
    )
    smol_quiz_male = relationship(
        'OrmSMOLQuiz',
        primaryjoin='and_(OrmCompatibilityQuiz.id==OrmSMOLQuiz.compatibility_quiz_id, OrmSMOLQuiz.is_male==True)',
        uselist=False
    )
    smol_quiz_female = relationship(
        'OrmSMOLQuiz',
        primaryjoin='and_(OrmCompatibilityQuiz.id==OrmSMOLQuiz.compatibility_quiz_id, OrmSMOLQuiz.is_male==False)',
        uselist=False
    )
