from sqlalchemy import Column, Integer, String, Boolean,ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from ..conf.database import Base

class Traduction(Base):
    __tablename__ = "traductions"
    id = Column(Integer, primary_key=True)
    key = Column((String(40)))
    value = Column((String(250)))
    dictionnary_id = Column(Integer, ForeignKey('dictionaries.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
   