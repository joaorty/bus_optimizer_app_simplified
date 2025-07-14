from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base

class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
    length_km = Column(Numeric(8, 2), nullable=False)
    time_minutes = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)

    scenario = relationship("Scenario", back_populates="routes")

    def __init__(self, scenario_id, length_km, time_minutes, passengers):
        self.scenario_id = scenario_id
        self.length_km = length_km
        self.time_minutes = time_minutes
        self.passengers = passengers

    def __repr__(self):
        return f"<Route(id={self.id}, scenario_id={self.scenario_id})>"

    def to_dict(self):
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "length_km": float(self.length_km),
            "time_minutes": self.time_minutes,
            "passengers": self.passengers,
        }
