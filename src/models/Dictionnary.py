from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from ..conf.database import Base
from sqlalchemy.sql import func


class Dictionnary(Base):
    __tablename__ = "dictionaries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column((String(40)))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    


