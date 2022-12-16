from fastapi import APIRouter


# from .orders import router as order_router
from .client import router as client_router
from .famaly_love_quiz import router as famaly_love_quiz_router


router = APIRouter(
    prefix="/v1"
)

@router.get(
    path='/todo'
)
async def get_todo():
    return {
        'Api model': True,
        'DAL model': True,
        'Service model': True,
        'Валидация': False,
        
        'DAL queries': 'Почти доделал',
        'Service': 'Делаю вместе с DAL',
        'Api route': 'Пути до роутов уже точно не буду менять, остальное сделаю после реализации записи в бд и предобработки.',
        
        'Processing quiz': 'Что тут вообще должно быть? Как обрабатывается опрос?',
        'Processing ML': 'Когда-то нужно сделать, но пока не знаю как. Возможно отдельный сервис будет. pubsub буду использовать',
    }

# router.include_router(
#     router=client_router, prefix="/client", tags=["client"]
# )
router.include_router(
    router=famaly_love_quiz_router, prefix="/famaly_love_quiz", tags=["famaly_love_quiz"]
)

