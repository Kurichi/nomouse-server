from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from schemas.user import UserId
from schemas.util import DeleteStatus

def create_user_handler(db: Session, google_uid:str) -> UserId:
  if google_uid == '':
    raise HTTPException(status_code=400, detail="Name is empty")

  result_by_google_uid = db.query(models.Users).filter(models.Users.google_uid == google_uid).first()
  if result_by_google_uid != None:
    raise HTTPException(
      status_code=400,
      detail="The tag is exist"
    )


  user_orm = models.Users(
    google_uid=google_uid
  )
  db.add(user_orm)
  db.commit()
  db.refresh(user_orm)

  tag = UserId.from_orm(user_orm)

  return tag

def get_user_handler(db: Session, google_uid: str) -> UserId:
  user_orm = db.query(models.Users).filter(models.Users.google_uid == google_uid).first()
  if user_orm is None:
    raise HTTPException(
      status_code=404,
      detail="The user specified by id is not exist"
    )
  user = UserId.from_orm(user_orm)
  return user


def delete_user_handler(db: Session, google_uid: str) -> UserId:
  slide_orm = db.query(models.Slides).filter(models.Slides.google_uid == google_uid).all()

  for slide in slide_orm:
    share_orm = db.query(models.ShareIds).filter(models.ShareIds.slide_id == slide.id).first()

    if share_orm != None:
      db.delete(share_orm)

    if slide_orm != None:
      db.delete(slide_orm)

  user_orm = db.query(models.Users).filter(models.Users.google_uid == google_uid).first()
  if user_orm == None:
    raise HTTPException(
      status_code=400,
      detail="The user is not exist"
    )

  db.delete(user_orm)
  db.commit()

  result = DeleteStatus(status="OK")

  return result
