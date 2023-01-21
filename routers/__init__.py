from fastapi import APIRouter
from .user import users
from .slide import slides
from .share import shares
from .assets import asset_router

router = APIRouter()

router.include_router(users, prefix='/users', tags=['users'])
router.include_router(slides, prefix='/slides', tags=['slides'])
router.include_router(shares, prefix='/share', tags=['shares'])
router.include_router(asset_router, prefix='/assets', tags=['assets'])
