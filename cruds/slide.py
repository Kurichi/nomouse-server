from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from schemas.slide import Slide
from schemas.util import DeleteStatus
from pydantic import Json
import json


def create_slide_handler(db: Session, google_uid:str, code: str, compiled_data: list[Json[any]], thumbnail: str) -> Slide:
  if google_uid == '':
    raise HTTPException(status_code=400, detail="No auth")

  slide_orm = models.Slides(
    google_uid=google_uid,
    code=code,
    compiled_data=compiled_data,
    thumbnail=thumbnail
  )
  db.add(slide_orm)
  db.commit()
  db.refresh(slide_orm)

  slide = Slide.from_orm(slide_orm)

  return slide


def change_slide_handler(db: Session, google_uid:str, slide_id: str, code: str, compiled_data: list[Json[any]], thumbnail: str) -> Slide:
  if google_uid == '':
    raise HTTPException(status_code=400, detail="No auth")

  slide_orm = db.query(models.Slides).filter(models.Slides.id == slide_id).first()
  if slide_orm == None:
    raise HTTPException(
      status_code=400,
      detail="The slide is not exist"
    )

  slide_orm.code = slide_orm.code if code is None else code
  slide_orm.compiled_data = slide_orm.compiled_data if compiled_data is None else compiled_data
  slide_orm.thumbnail = slide_orm.thumbnail if thumbnail is None else thumbnail

  db.commit()
  db.refresh(slide_orm)

  slide = Slide.from_orm(slide_orm)

  return slide


def get_slides_handler(db: Session, google_uid: str) -> list[Slide]:
  slides_orm = db.query(models.Slides).filter(models.Slides.google_uid == google_uid).all()

  slides = list(map(Slide.from_orm, slides_orm))
  return slides

def get_slide_handler(db: Session, google_uid: str, slide_id: str) -> Slide:
  slide_orm = db.query(models.Slides).filter(models.Slides.google_uid == google_uid).filter(models.Slides.id == slide_id).first()
  if slide_orm is None:
    raise HTTPException(
      status_code=404,
      detail="The slide specified by id is not exist"
    )
  slide = Slide.from_orm(slide_orm)
  return slide


def delete_slide_handler(db: Session, google_uid: str, slide_id: str) -> DeleteStatus:
  result = DeleteStatus(status="OK")

  share_orm = db.query(models.ShareIds).filter(models.ShareIds.slide_id == slide_id).first()

  if share_orm != None:
    db.delete(share_orm)

  slide_orm = db.query(models.Slides).filter(models.Slides.google_uid == google_uid).filter(models.Slides.id == slide_id).first()

  if slide_orm != None:
    db.delete(slide_orm)
    db.commit()
  else:
    result.status="No exist"

  return result
