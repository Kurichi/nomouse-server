from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter
from fastapi.params import Depends
from cruds.share import get_share_handler, create_share_handler, delete_share_handler
from cruds.firebase_auth import GetCurrentUser
from schemas.share import Share
from schemas.slide import Slide
from schemas.user import UserId
from schemas.util import DeleteStatus

shares = APIRouter()

@shares.get('/',response_model=Slide)
async def get_share(shared_id: str = '', db: Session = Depends(get_db)):
  result = get_share_handler(db, shared_id)
  return result

@shares.post('/', response_model=Share)
async def post_share(slide_id: str = '', db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = create_share_handler(db, user.google_uid, slide_id)
  return result

@shares.delete('/', response_model=DeleteStatus)
async def delete_share(slide_id: str = '', db: Session = Depends(get_db), user: UserId = Depends(GetCurrentUser())):
  result = delete_share_handler(db, user.google_uid, slide_id)
  return result
