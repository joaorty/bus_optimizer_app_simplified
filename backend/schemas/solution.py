from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class SolutionBase(BaseModel):
  scenario_id: int
  status: Literal["Pending", "Running", "Completed", "Failed"] = "Pending"
  objective_value: Optional[float] = None
  solution_data: Optional[dict] = None
  parameters_solution: Optional[dict] = None

class SolutionCreate(SolutionBase):
  pass

class SolutionRead(SolutionBase):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True
