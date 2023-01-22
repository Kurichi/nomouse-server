from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter
from fastapi.params import Depends
from cruds.slide import get_slide_handler, create_slide_handler, change_slide_handler, delete_slide_handler, get_slides_handler
from cruds.firebase_auth import GetCurrentUser
from schemas.slide import Slide, PostSlide, PutSlide
from schemas.user import UserId
from schemas.util import DeleteStatus

slides = APIRouter()

@slides.get('/', response_model=list[Slide])
async def get_all_slide(db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = get_slides_handler(db, user.google_uid)
  return result

@slides.get('/{slide_id}',response_model=Slide)
async def get_slide(slide_id: str = '', db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = get_slide_handler(db, user.google_uid, slide_id)
  return result

@slides.post('/', response_model=Slide)
async def post_slide(payload: PostSlide, db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = create_slide_handler(db, user.google_uid, payload.code, payload.compiled_data, payload.thumbnail, payload.title)
  return result

@slides.put('/', response_model=Slide)
async def change_user(payload: PutSlide, db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = change_slide_handler(db, user.google_uid, payload.slide_id, payload.code, payload.compiled_data, payload.thumbnail, payload.title)
  return result

@slides.delete('/', response_model=DeleteStatus)
async def delete_slide(slide_id: str = '', db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = delete_slide_handler(db, user.google_uid, slide_id)
  return result
