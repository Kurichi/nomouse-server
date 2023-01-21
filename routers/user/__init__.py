from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from cruds.user import get_user_handler, create_user_handler, delete_user_handler
from cruds.firebase_auth import GetCurrentUser
from schemas.user import UserId
from schemas.util import DeleteStatus
from db import models

users = APIRouter()

@users.get('/',response_model=UserId)
async def get_user(db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = get_user_handler(db, user.google_uid)
  return result

@users.post('/', response_model=UserId)
async def post_user(payload: UserId, db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  if (payload.google_uid != user.google_uid):
    raise HTTPException(
      status_code=400,
      detail="ID is incorrect"
    )
  result = create_user_handler(db, user.google_uid)
  return result

@users.delete('/', response_model=DeleteStatus)
async def delete_user(db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = delete_user_handler(db, user.google_uid)
  return result
