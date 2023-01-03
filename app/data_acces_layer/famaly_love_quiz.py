from sqlalchemy.ext.asyncio import AsyncSession
from models.database import OrmClient, OrmFamalyLoveQuiz
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from .abstract import AbstractDALFamalyLoveQuiz
from functools import lru_cache
from typing import Optional, List
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeasEnum


class DALFamalyLoveQuiz(AbstractDALFamalyLoveQuiz):
    async def create(
        self: 'DALFamalyLoveQuiz',
        compatibility_quiz_id: int,
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
        session: AsyncSession,
    ) -> OrmFamalyLoveQuiz:
        orm_famaly_love_quiz = OrmFamalyLoveQuiz(
            compatibility_quiz_id=compatibility_quiz_id,
            height_difference=height_difference,
            weight_difference=weight_difference,
            age_difference=age_difference,
            alcoholism=alcoholism,
            political_views_difference=political_views_difference,
            leisure_preferences_coincide=leisure_preferences_coincide,
            education_level=education_level,
            salary_male=salary_male,
            salary_female=salary_female,
            housing=housing,
            explore_together=explore_together,
            exchange_ideas=exchange_ideas,
            economy_sector_male=economy_sector_male,
            economy_sector_female=economy_sector_female
        )
        session.add(orm_famaly_love_quiz)
        await session.flush()
        await session.refresh(orm_famaly_love_quiz)
        return orm_famaly_love_quiz

    async def get_by_id(
        self: 'DALFamalyLoveQuiz',
        id: int,
        session: AsyncSession
    ) -> OrmFamalyLoveQuiz:
        orm_famaly_love_quiz = await session.execute(
            select(OrmFamalyLoveQuiz)
            .options(selectinload(OrmFamalyLoveQuiz.images))
            .where(OrmFamalyLoveQuiz.id == id)
        )
        return orm_famaly_love_quiz.scalar()

    async def get_count(
        self: 'DALFamalyLoveQuiz',
        session: AsyncSession
    ) -> int:
        count = await session.execute(
            select(
                func.count()
            )
            .select_from(OrmFamalyLoveQuiz)
        )
        return count.scalar()

    # async def update_by_id(
    #     self: 'DALFamalyLoveQuiz',
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
    #     exchange_ideas: Optional[ExchangeIdeasEnum] = None,
    #     economy_sector_male: Optional[List[int]] = None,
    #     economy_sector_female: Optional[List[int]] = None,
    #     is_send_to_email: Optional[bool] = None,
    #     is_consent_to_data_processing: Optional[bool] = None,
    #     email: Optional[str] = None,
    # ) -> OrmFamalyLoveQuiz:
    #     async with _postgres_async_session() as session:
    #         await session.execute(
    #             select(OrmFamalyLoveQuiz)
    #             .options(selectinload(OrmFamalyLoveQuiz.images))
    #             .where(OrmClient.id == id)
    #         )
    #         return self.get_by_id(id)

    async def delete_by_id(
        self: 'DALFamalyLoveQuiz',
        id: int,
        session: AsyncSession
    ) -> OrmFamalyLoveQuiz:
        orm_famaly_love_quiz = await session.execute(
            select(OrmFamalyLoveQuiz)
            .options(selectinload(OrmFamalyLoveQuiz.images))
            .where(OrmFamalyLoveQuiz.id == id)
        )
        if not orm_famaly_love_quiz:
            return None
        await session.delete(orm_famaly_love_quiz)


@lru_cache()
def get_DAL_famaly_love_quiz() -> DALFamalyLoveQuiz:
    return DALFamalyLoveQuiz()
