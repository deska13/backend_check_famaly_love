from fastapi import APIRouter, Depends
from services import (
    ClientService, get_client_service,
    CompatibilityQuizService, get_compatibility_quiz_service,
    FamalyLoveImageService, get_famaly_love_image_service,
    FamalyLoveQuizService, get_famaly_love_quiz,
    MBTIQuizService, get_mbti_quiz_service,
    SMOLQuizService, get_smol_quiz_service
)
from .models import CompatibilityQuiz, ResultCompatibilityQuiz, StatusProcessingCompatibilityQuizEnum, FamalyLoveImages
from data_acces_layer import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeasEnum

router = APIRouter()


@router.post(
    path='/',
    # response_model=FamalyLoveQuizId
)
async def send_quiz_famaly_love(
    compatibility_quiz: CompatibilityQuiz,
    client_service: ClientService = Depends(
        get_client_service),
    compatibility_quiz_service: CompatibilityQuizService = Depends(
        get_compatibility_quiz_service),
    famaly_love_image_service: FamalyLoveImageService = Depends(
        get_famaly_love_image_service),
    famaly_love_quiz_service: FamalyLoveQuizService = Depends(
        get_famaly_love_quiz),
    mbti_quiz_service: MBTIQuizService = Depends(
        get_mbti_quiz_service),
    smol_quiz_service: SMOLQuizService = Depends(
        get_smol_quiz_service),
    session: AsyncSession = Depends(get_session)
):
    orm_client = await client_service.create(session=session)
    orm_compatibility_quiz = await compatibility_quiz_service.create(
        orm_client.id,
        is_send_to_email=compatibility_quiz.is_send_to_email,
        email=compatibility_quiz.email,
        session=session
    )
    orm_famaly_love_quiz_service = await famaly_love_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.famaly_love_quiz.dict(),
        session=session
    )
    for male_image in compatibility_quiz.images.male_images:
        orm_famaly_love_image = await famaly_love_image_service.create(
            orm_famaly_love_quiz_service.id,
            is_male=True,
            image_path=male_image,
            session=session
        )
    for female_image in compatibility_quiz.images.female_images:
        orm_famaly_love_image = await famaly_love_image_service.create(
            orm_famaly_love_quiz_service.id,
            is_male=False,
            image_path=female_image,
            session=session
        )
    orm_mbti_female = await mbti_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.mbti_quiz_female.dict(),
        is_male=False,
        session=session
    )
    orm_mbti_male = await mbti_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.mbti_quiz_male.dict(),
        is_male=True,
        session=session
    )
    orm_smol_female = await smol_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.smol_quiz_female.dict(),
        is_male=False,
        session=session
    )
    orm_smol_male = await smol_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.smol_quiz_male.dict(),
        is_male=True,
        session=session
    )
    try:
        await session.commit()
        return orm_compatibility_quiz.id
    except IntegrityError as ex:
        await session.rollback()
        raise ex


@router.get(
    path='/{id}/result',
    response_model=ResultCompatibilityQuiz
)
async def get_result(
    id: int,
    compatibility_quiz_service: CompatibilityQuizService = Depends(
        get_compatibility_quiz_service),
    session: AsyncSession = Depends(get_session)
):
    compatibility_quiz = await compatibility_quiz_service.get_by_id(id=id, session=session)

    count_famaly_years = 1
    famaly_love_quiz = compatibility_quiz.famaly_love_quiz
    if famaly_love_quiz.height_difference < -20:
        count_famaly_years -= 3
    elif famaly_love_quiz.height_difference < 0:
        count_famaly_years -= round(
            abs(famaly_love_quiz.height_difference) / 20 * 3)
    elif famaly_love_quiz.height_difference < 12:
        count_famaly_years += round(
            abs(famaly_love_quiz.height_difference) / 12 * 3)
    elif famaly_love_quiz.height_difference < 20:
        count_famaly_years += round(abs(20 -
                                    famaly_love_quiz.height_difference) / 8 * 3)

    if famaly_love_quiz.weight_difference < -20:
        count_famaly_years -= 3
    elif famaly_love_quiz.weight_difference < 0:
        count_famaly_years -= round(
            abs(famaly_love_quiz.weight_difference) / 20 * 3)
    elif famaly_love_quiz.weight_difference < 10:
        count_famaly_years += round(
            abs(famaly_love_quiz.weight_difference) / 10 * 3)
    elif famaly_love_quiz.weight_difference < 15:
        count_famaly_years += round(abs(15 -
                                    famaly_love_quiz.weight_difference) / 5 * 3)

    if famaly_love_quiz.age_difference < -10:
        count_famaly_years -= 2
    elif famaly_love_quiz.age_difference < -7:
        count_famaly_years -= round(abs(10 -
                                    famaly_love_quiz.age_difference) / 3 * 2)
    elif famaly_love_quiz.age_difference < 0:
        count_famaly_years += round(abs(famaly_love_quiz.age_difference) / 7 * 5)
    elif famaly_love_quiz.age_difference < 6:
        count_famaly_years += round(abs(famaly_love_quiz.age_difference) / 6 * 5)
    elif famaly_love_quiz.age_difference < 10:
        count_famaly_years -= round(abs(10 -
                                    famaly_love_quiz.age_difference) / 4 * 3)
    else:
        count_famaly_years -= 3

    if famaly_love_quiz.alcoholism:
        count_famaly_years -= 4
    else:
        count_famaly_years += 4

    if famaly_love_quiz.political_views_difference:
        count_famaly_years -= 2
    else:
        count_famaly_years += 2

    if famaly_love_quiz.leisure_preferences_coincide == LeisurePreferencesCoincideEnum.YES:
        count_famaly_years += 3
    elif famaly_love_quiz.leisure_preferences_coincide == LeisurePreferencesCoincideEnum.NO:
        count_famaly_years -= 3

    if famaly_love_quiz.education_level == EducationLevelEnum.YES:
        count_famaly_years += 3
    else:
        count_famaly_years -= 3

    if famaly_love_quiz.salary_male - famaly_love_quiz.salary_female != 0:
        percent_different_salary = (1 - (famaly_love_quiz.salary_male /
                                         (famaly_love_quiz.salary_male - famaly_love_quiz.salary_female))) * 100
        print(percent_different_salary)
        if percent_different_salary < -30:
            count_famaly_years -= 2
        elif percent_different_salary < -15:
            count_famaly_years -= round(abs(30 -
                                        percent_different_salary) / 15 * 2)
        elif percent_different_salary < 17:
            count_famaly_years += round(
                abs(percent_different_salary - 17) / 32 * 3)
        elif percent_different_salary < 50:
            count_famaly_years += round(
                abs(percent_different_salary - 17) / 33 * 1)
    else:
        count_famaly_years -= 2

    if famaly_love_quiz.housing == HousingEnum.YES:
        count_famaly_years += 4
    elif famaly_love_quiz.housing == HousingEnum.MORTAGE:
        count_famaly_years -= 2
    elif famaly_love_quiz.housing == HousingEnum.NO:
        count_famaly_years += 1

    if famaly_love_quiz.explore_together == ExploreTogetherEnum.YES:
        count_famaly_years += 3
    elif famaly_love_quiz.explore_together == ExploreTogetherEnum.SOMETIMES:
        count_famaly_years += 1
    elif famaly_love_quiz.explore_together == ExploreTogetherEnum.NO:
        count_famaly_years -= 1

    if famaly_love_quiz.exchange_ideas == ExchangeIdeasEnum.YES:
        count_famaly_years += 3
    elif famaly_love_quiz.exchange_ideas == ExchangeIdeasEnum.SOMETIMES:
        count_famaly_years += 1
    elif famaly_love_quiz.exchange_ideas == ExchangeIdeasEnum.NO:
        count_famaly_years -= 2

    flag = False
    for i in famaly_love_quiz.economy_sector_male:
        for j in famaly_love_quiz.economy_sector_female:
            if i == j:
                flag = True
    if flag:
        count_famaly_years += 5

    compatibility_quiz.mbti_quiz_male
    compatibility_quiz.mbti_quiz_female
    compatibility_quiz.smol_quiz_male
    compatibility_quiz.smol_quiz_female

    count_famaly_years = count_famaly_years if 0 < count_famaly_years else 0

    return ResultCompatibilityQuiz(
        status=StatusProcessingCompatibilityQuizEnum.OK,
        description=f'{count_famaly_years} лет'
    )

    return count_famaly_years


@router.get(
    path='/{id}/images',
    response_model=FamalyLoveImages
)
async def get_client_images(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return FamalyLoveImages(
        male_images=[
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWBAMAAADOL2zRAAAAG1BMVEUAAAv///+fn6NfX2YfHyk/P0h/f4W/v8Lf3+CfzlVWAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABAElEQVRoge3SMW+DMBiE4YsxJqMJtHOTITPeOsLQnaodGImEUMZEkZhRUqn92f0MaTubtfeMh/QGHANEREREREREREREtIJJ0xbH299kp8l8FaGtLdTQ19HjofxZlJ0m1+eBKZcikd9PWtXC5DoDotRO04B9YOvFIXmXLy2jEbiqE6Df7DTleA5socLqvEFVxtJyrpZFWz/pHM2CVte0lS8g2eDe6prOyqPglhzROL+Xye4tmT4WvRcQ2/m81p+/rdguOi8Hc5L/8Qk4vhZzy08DduGt9eVQyP2qoTM1zi0/uf4hvBWf5c77e69Gf798y08L7j0RERERERERERH9P99ZpSVRivB/rgAAAABJRU5ErkJggg=='
        ],
        female_images=[
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWBAMAAADOL2zRAAAAG1BMVEUAAAv///+fn6NfX2YfHyk/P0h/f4W/v8Lf3+CfzlVWAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABAElEQVRoge3SMW+DMBiE4YsxJqMJtHOTITPeOsLQnaodGImEUMZEkZhRUqn92f0MaTubtfeMh/QGHANEREREREREREREtIJJ0xbH299kp8l8FaGtLdTQ19HjofxZlJ0m1+eBKZcikd9PWtXC5DoDotRO04B9YOvFIXmXLy2jEbiqE6Df7DTleA5socLqvEFVxtJyrpZFWz/pHM2CVte0lS8g2eDe6prOyqPglhzROL+Xye4tmT4WvRcQ2/m81p+/rdguOi8Hc5L/8Qk4vhZzy08DduGt9eVQyP2qoTM1zi0/uf4hvBWf5c77e69Gf798y08L7j0RERERERERERH9P99ZpSVRivB/rgAAAABJRU5ErkJggg=='
        ]
    )


@router.put(
    path='/{id}/images'
)
async def reinit_images(
    id: int,
    images: FamalyLoveImages,
    session: AsyncSession = Depends(get_session)
):
    return id, images
