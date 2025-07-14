from sqlalchemy import Column, Integer, ForeignKey, Numeric
from .base import Base

class Route(Base):
  __tablename__ = "route"

  id = Column(Integer, primary_key=True, index=True)
  scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
  length_km = Column(Numeric(8, 2), nullable=False)
  time_minutes = Column(Integer, nullable=False)
  passengers = Column(Integer, nullable=False)
