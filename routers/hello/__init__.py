from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter
from fastapi.params import Depends
# from schemas.work import Work
# from schemas.user import User, UserInfoChangeRequest
from db import models

hello = APIRouter()

@hello.get('/')
async def get_me():
  return {"text": "hello"}