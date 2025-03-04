from fastapi import APIRouter
from .users import router as users_router
from .fake_news import router as fake_news_router
from .detection import router as detection_router
from .admin import router as admin_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(fake_news_router, prefix="/fake-news", tags=["Fake News"])
router.include_router(detection_router, prefix="/detection", tags=["Detection"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])
