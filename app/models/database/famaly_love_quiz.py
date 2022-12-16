from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, Boolean, ARRAY, Enum
from sqlalchemy.orm import relationship

from ._base import BaseOrmModel
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeas


class OrmFamalyLoveQuiz(BaseOrmModel):
    __tablename__ = "famaly_love_quiz"

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
    leisure_preferences_coincide = Column(Enum(LeisurePreferencesCoincideEnum))
    education_level = Column(Enum(EducationLevelEnum))
    salary_male = Column(Integer)
    salary_female = Column(Integer)
    housing = Column(Enum(HousingEnum))
    explore_together = Column(Enum(ExploreTogetherEnum))
    exchange_ideas = Column(Enum(ExchangeIdeas))
    economy_sector_male = Column(ARRAY(Integer))
    economy_sector_female = Column(ARRAY(Integer))

    is_send_to_email = Column(Boolean)
    is_shipped = Column(Boolean)

    email = Column(Text)

    is_ml_processing = Column(Boolean)
    is_quiz_processing = Column(Boolean)
    result = Column(Text)

    images = relationship("OrmImage")
    client = relationship("OrmClient")
