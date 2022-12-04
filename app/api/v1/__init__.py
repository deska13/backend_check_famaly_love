from fastapi import APIRouter


# from .orders import router as order_router
from .client import router as client_router


router = APIRouter(
    prefix="/v1"
)
router.include_router(
    router=client_router, prefix="/client", tags=["client"]
)