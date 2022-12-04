from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class Client(BaseOrmModel):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )

    batch_param = relationship("OrmBatchType")
    pallets = relationship("OrmPallet", cascade="all, delete")
    products = relationship("OrmProduct", cascade="all, delete")