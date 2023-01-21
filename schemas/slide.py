from pydantic import BaseModel, Json
from datetime import datetime
from typing import Any

class PostSlide(BaseModel):
  code: str
  compiled_data: str
  thumbnail: str

  class Config:
    orm_mode = True

class PutSlide(BaseModel):
  slide_id: str
  code: str
  compiled_data: str
  thumbnail: str
  
  class Config:
    orm_mode = True

class Slide(BaseModel):
  id: str
  google_uid: str
  code: str
  compiled_data: str
  thumbnail: str
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True
