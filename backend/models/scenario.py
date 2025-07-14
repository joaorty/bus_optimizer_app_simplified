from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from .base import Base

class Scenario(Base):
  __tablename__ = "scenario"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(Text, nullable=False)
  description = Column(Text)
  created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
  updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
