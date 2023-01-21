from typing import Any
from sqlalchemy import Column as Col, String, Enum, ForeignKey, DateTime, Boolean, Integer, Text, JSON
from uuid import uuid4
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
import enum
import datetime
from sqlalchemy.sql.functions import func

class Column(Col):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)

def generate_uuid():
    return str(uuid4())

@as_declarative()
class Base:
    id: Any
    __name__: Any

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class Users(Base):

    __tablename__ = "users"

    google_uid = Column(String(length=255), primary_key=True)


class Slides(Base):

    __tablename__ = "slides"

    id = Column(String(length=255), primary_key=True, default=generate_uuid)
    google_uid = Column(String(length=255), ForeignKey('users.google_uid'))
    code = Column(Text())
    compiled_data = Column(JSON())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ShareIds(Base):

    __tablename__ = "share_ids"

    slide_id = Column(String(length=255), ForeignKey('slides.id'), primary_key=True)
    share_id = Column(String(length=255), primary_key=True, default=generate_uuid)
    
