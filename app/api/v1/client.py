from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get(
    path='/status'
)
async def get_status_client():
    return 0


@router.get(
    path='/{id}/processing_promblems'
)
async def get_processing_promblems(
    id: int
):
    return 0


@router.get(
    path='/{id}/result'
)
async def get_result(
    id: int
):
    return 0


@router.post(
    path='/'
)
async def create_client():
    return 0


@router.put(
    path='/{id}/images'
)
async def reinit_images(
    id: int
):
    return 0