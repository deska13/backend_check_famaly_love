import enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel


class PolitViewEnum(enum.Enum):
    no: 'no'
    yes: 'yes'


class Client(BaseOrmModel):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False, index=True
    )
    height_difference = Column(Integer)
    weight_difference = Column(Integer)
    age_difference = Column(Integer)
    alcoholism = Column(Boolean)
    political_views_difference = Column(PolitViewEnum)
    leisure_preferences_coincide = Column(Text)
    education_level = Column(Boolean)
    salary_male = Column()
    salary_female = Column()
    housing = Column()
    explore_together = Column()
    exchange_ideas = Column()
    economy_sector_male = Column()
    economy_sector_female = Column()
    
    
    
    

    client = relationship("Client")
