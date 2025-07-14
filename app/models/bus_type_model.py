from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base

class BusType(Base):
    __tablename__ = "bus_type"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
    seat_capacity = Column(Integer, nullable=False)
    operational_cost_km = Column(Numeric(4, 2), nullable=False)
    load_factor = Column(Numeric(4, 2), nullable=False)
    available_units = Column(Integer, nullable=False)

    scenario = relationship("Scenario", back_populates="bus_types")

    def __init__(self, scenario_id, seat_capacity, operational_cost_km, load_factor, available_units):
        self.scenario_id = scenario_id
        self.seat_capacity = seat_capacity
        self.operational_cost_km = operational_cost_km
        self.load_factor = load_factor
        self.available_units = available_units

    def __repr__(self):
        return f"<BusType(id={self.id}, scenario_id={self.scenario_id})>"

    def to_dict(self):
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "seat_capacity": self.seat_capacity,
            "operational_cost_km": float(self.operational_cost_km),
            "load_factor": float(self.load_factor),
            "available_units": self.available_units,
        }
