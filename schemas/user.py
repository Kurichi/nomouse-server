from pydantic import BaseModel

class UserId(BaseModel):
  google_uid: str

  class Config:
    orm_mode = True
