from fastapi import APIRouter
from .user import users
from .slide import slides

router = APIRouter()

router.include_router(users, prefix='/users', tags=['users'])
router.include_router(slides, prefix='/slides', tags=['slides'])
