from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean, ARRAY
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel
from ..quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeas


class OrmQuiz(BaseOrmModel):
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
    political_views_difference = Column(Boolean)
    leisure_preferences_coincide = Column(LeisurePreferencesCoincideEnum)
    education_level = Column(EducationLevelEnum)
    salary_male = Column(Integer)
    salary_female = Column(Integer)
    housing = Column(HousingEnum)
    explore_together = Column(ExploreTogetherEnum)
    exchange_ideas = Column(ExchangeIdeas)
    economy_sector_male = Column(ARRAY(Integer))
    economy_sector_female = Column(ARRAY(Integer))

    client = relationship("OrmClient")
