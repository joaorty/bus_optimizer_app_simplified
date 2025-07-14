from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, Enum, Numeric, JSON
from sqlalchemy.orm import relationship
import enum
from .base import Base

class SolutionStatus(str, enum.Enum):
    pending = "Pending"
    running = "Running"
    completed = "Completed"
    failed = "Failed"

class Solution(Base):
    __tablename__ = "solution"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(Enum(SolutionStatus), nullable=False, default=SolutionStatus.pending)
    objective_value = Column(Numeric(15, 2))
    solution_data = Column(JSON)
    parameters_solution = Column(JSON)

    scenario = relationship("Scenario", back_populates="solutions")

    def __init__(self, scenario_id, status=SolutionStatus.pending, objective_value=None, solution_data=None, parameters_solution=None):
        self.scenario_id = scenario_id
        self.status = status
        self.objective_value = objective_value
        self.solution_data = solution_data
        self.parameters_solution = parameters_solution

    def __repr__(self):
        return f"<Solution(id={self.id}, status={self.status})>"

    def to_dict(self):
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "objective_value": float(self.objective_value) if self.objective_value is not None else None,
            "solution_data": self.solution_data,
            "parameters_solution": self.parameters_solution,
        }
