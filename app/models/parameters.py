from sqlalchemy import Column, Integer, ForeignKey, Numeric
from .base import Base

class Parameters(Base):
  __tablename__ = "parameters"

  id = Column(Integer, primary_key=True, index=True)
  scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
  units_time = Column(Integer, nullable=False)
  wait_cost = Column(Numeric(6, 2), nullable=False)
  agglomeration_cost = Column(Numeric(6, 2), nullable=False)
  acceptable_time_transfer = Column(Integer, nullable=False)
