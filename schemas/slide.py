from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime

class Slide(BaseModel):
  id: str
  google_uid: str
  code: str
  code: list[Json[any]]
  created_at: datetime
  updated_at: datetime
