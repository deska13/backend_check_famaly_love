from fastapi import APIRouter


# from .orders import router as order_router
from .client import router as client_router
from .compatibility_quiz import router as compatibility_quiz_router


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
        'Api route': True,

        'Processing quiz': 'Что тут вообще должно быть? Как обрабатывается опрос?',
        'Processing ML': True,

        'Test': False
    }

# router.include_router(
#     router=client_router, prefix="/client", tags=["client"]
# )
router.include_router(
    router=compatibility_quiz_router, prefix="/compatibility_quiz", tags=["compatibility_quiz"]
)
