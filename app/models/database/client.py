from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmClient(BaseOrmModel):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )
    email = Column(Text)

    images = relationship("OrmImage")
    order = relationship("OrmOrder", cascade="all, delete")
    quiz = relationship("OrmQuiz", cascade="all, delete")