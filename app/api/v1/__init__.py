from fastapi import APIRouter


from .orders import router as order_router


router = APIRouter(prefix="/v1")
router.include_router(
    router=order_router, prefix="/order", tags=["order"]
)