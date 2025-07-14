from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, Enum, Numeric, JSON
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
