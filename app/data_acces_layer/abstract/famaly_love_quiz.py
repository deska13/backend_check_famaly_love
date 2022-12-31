from abc import abstractmethod
from typing import Optional, List
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeasEnum

from ._base import BaseAbstractDataAccessLayer


class AbstractDALFamalyLoveImage(BaseAbstractDataAccessLayer):
    @abstractmethod
    async def create(
        self: 'AbstractDALFamalyLoveImage',
        height_difference: int,
        weight_difference: int,
        age_difference: int,
        alcoholism: bool,
        political_views_difference: bool,
        leisure_preferences_coincide: LeisurePreferencesCoincideEnum,
        education_level: EducationLevelEnum,
        salary_male: int,
        salary_female: int,
        housing: HousingEnum,
        explore_together: ExploreTogetherEnum,
        exchange_ideas: ExchangeIdeasEnum,
        economy_sector_male: List[int],
        economy_sector_female: List[int],
        images: int,
        is_send_to_email: bool,
        is_consent_to_data_processing: bool,
        email: Optional[str] = None
    ) -> None:
        pass

    # @abstractmethod
    # async def update_by_id(
    #     self: 'AbstractDALFamalyLoveImage',
    #     id: int,
    #     height_difference: Optional[int] = None,
    #     weight_difference: Optional[int] = None,
    #     age_difference: Optional[int] = None,
    #     alcoholism: Optional[bool] = None,
    #     political_views_difference: Optional[bool] = None,
    #     leisure_preferences_coincide: Optional[LeisurePreferencesCoincideEnum] = None,
    #     education_level: Optional[EducationLevelEnum] = None,
    #     salary_male: Optional[int] = None,
    #     salary_female: Optional[int] = None,
    #     housing: Optional[HousingEnum] = None,
    #     explore_together: Optional[ExploreTogetherEnum] = None,
    #     exchange_ideas: Optional[ExchangeIdeas] = None,
    #     economy_sector_male: Optional[List[int]] = None,
    #     economy_sector_female: Optional[List[int]] = None,
    #     images: Optional[int] = None,
    #     is_send_to_email: Optional[bool] = None,
    #     is_consent_to_data_processing: Optional[bool] = None,
    #     email: Optional[str] = None
    # ) -> None:
    #     pass
