from fastapi import APIRouter
from .models import ClientId


router = APIRouter()


# @router.post(
#     path='/create',
# )
# async def create_client():
#     return 'Оно просто существует'


@router.get(
    path='/{id}',
    response_model=ClientId
)
async def get_client(
    id: int
):
    return ClientId(client_id=id)


@router.get(
    path='/count',
    response_model=int
)
async def get_count():
    return 0
