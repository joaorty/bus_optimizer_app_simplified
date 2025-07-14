from sqlalchemy import Column, Integer, ForeignKey, Numeric
from .base import Base

class BusType(Base):
  __tablename__ = "bus_type"

  id = Column(Integer, primary_key=True, index=True)
  scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
  seat_capacity = Column(Integer, nullable=False)
  operational_cost_km = Column(Numeric(4, 2), nullable=False)
  load_factor = Column(Numeric(4, 2), nullable=False)
  available_units = Column(Integer, nullable=False)
