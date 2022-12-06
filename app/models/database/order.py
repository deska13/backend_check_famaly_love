from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class OrmOrder(BaseOrmModel):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )
    is_pay = Column(Boolean, default=False)

    client = relationship("OrmClient")
