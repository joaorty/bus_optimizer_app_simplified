from pydantic import BaseModel

class ParametersBase(BaseModel):
  scenario_id: int
  units_time: int
  wait_cost: float
  agglomeration_cost: float
  acceptable_time_transfer: int

class ParametersCreate(BaseModel):
  units_time: int
  wait_cost: float
  agglomeration_cost: float
  acceptable_time_transfer: int

class ParametersRead(ParametersBase):
  id: int

  class Config:
    orm_mode = True