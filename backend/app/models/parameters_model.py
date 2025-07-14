from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.utils import Base

class Parameters(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
    units_time = Column(Integer, nullable=False)
    wait_cost = Column(Numeric(6, 2), nullable=False)
    agglomeration_cost = Column(Numeric(6, 2), nullable=False)
    acceptable_time_transfer = Column(Integer, nullable=False)

    scenario = relationship("Scenario", back_populates="parameters")

    def __init__(self, scenario_id, units_time, wait_cost, agglomeration_cost, acceptable_time_transfer):
        self.scenario_id = scenario_id
        self.units_time = units_time
        self.wait_cost = wait_cost
        self.agglomeration_cost = agglomeration_cost
        self.acceptable_time_transfer = acceptable_time_transfer

    def __repr__(self):
        return f"<Parameters(id={self.id}, scenario_id={self.scenario_id})>"

    def to_dict(self):
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "units_time": self.units_time,
            "wait_cost": float(self.wait_cost),
            "agglomeration_cost": float(self.agglomeration_cost),
            "acceptable_time_transfer": self.acceptable_time_transfer,
        }
