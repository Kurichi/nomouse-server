from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from schemas.slide import Slide
from schemas.share import Share
from schemas.util import DeleteStatus
from pydantic import Json
import json


def create_share_handler(db: Session, google_uid:str, slide_id: str) -> Share:
  if google_uid == '':
    raise HTTPException(status_code=400, detail="No auth")

  share_orm = models.ShareIds(
    slide_id = slide_id
  )

  db.add(share_orm)
  db.commit()
  db.refresh(share_orm)

  share = Share.from_orm(share_orm)

  return share


def get_share_handler(db: Session, shared_id: str) -> Slide:
  share_orm = db.query(models.ShareIds).filter(models.ShareIds.share_id == shared_id).first()
  if share_orm is None:
    raise HTTPException(
      status_code=404,
      detail="The slide specified by id is not exist"
    )

  slide_orm = db.query(models.Slides).filter(models.Slides.id == share_orm.slide_id).first()
  if slide_orm is None:
    raise HTTPException(
      status_code=404,
      detail="The slide specified by id is not exist"
    )
  slide = Slide.from_orm(slide_orm)
  return slide


def delete_share_handler(db: Session, google_uid: str, slide_id: str) -> DeleteStatus:
  result = DeleteStatus(status="OK")

  share_orm = db.query(models.ShareIds).filter(models.ShareIds.slide_id == slide_id).first()

  if share_orm != None:
    db.delete(share_orm)
  else:
    result.status="No exist"

  slide_orm = db.query(models.Slides).filter(models.Slides.google_uid == google_uid).filter(models.Slides.id == slide_id).first()
  if slide_orm != None:
    db.commit()
  else:
    result.status="IT IS NOT YOUR SLIDE"

  return result
