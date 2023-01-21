from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime

class Share(BaseModel):
    slide_id: str
    share_id: str

    class Config:
        orm_mode = True
