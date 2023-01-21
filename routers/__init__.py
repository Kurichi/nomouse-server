from fastapi import APIRouter
from .hello import hello

router = APIRouter()

router.include_router(hello, prefix='/hello', tags=['hello'])
