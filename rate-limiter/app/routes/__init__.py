from fastapi import APIRouter

from .users import router as users_router
from .students import router as students_router

router = APIRouter()

router.include_router(users_router)
router.include_router(students_router)