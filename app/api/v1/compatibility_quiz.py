from fastapi import APIRouter, Depends
from services import FamalyLoveQuizService, get_famaly_love_quiz
from .models import CompatibilityQuiz, ResultCompatibilityQuiz, StatusProcessingCompatibilityQuizEnum, FamalyLoveImages

router = APIRouter()


@router.post(
    path='/',
    #response_model=FamalyLoveQuizId
)
async def send_quiz_famaly_love(
    compatibility_quiz_router_quiz: CompatibilityQuiz,
    compatibility_quiz_service: FamalyLoveQuizService = Depends(get_famaly_love_quiz)
):
    return compatibility_quiz_router_quiz
    famaly_love_quiz = await famaly_love_quiz_service.create(
        **famaly_love_quiz.dict()
    )
    return FamalyLoveQuiz.parse_obj(famaly_love_quiz)


@router.get(
    path='/{id}/result',
    response_model=ResultCompatibilityQuiz
)
async def get_result(
    id: int
):
    return ResultCompatibilityQuiz(
        status=StatusProcessingCompatibilityQuizEnum.ERROR,
        traceback='Сервис не реализован',
        description='Текст'
    )


@router.get(
    path='/{id}/images',
    response_model=FamalyLoveImages
)
async def get_client_images(
    id: int
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
    images: FamalyLoveImages
):
    return id, images
