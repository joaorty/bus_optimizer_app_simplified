from pydantic import BaseModel

class RouteBase(BaseModel):
  scenario_id: int
  length_km: float
  time_minutes: int
  passengers: int

class RouteCreate(BaseModel):
  length_km: float
  time_minutes: int
  passengers: int

class RouteRead(RouteBase):
  id: int

  class Config:
    orm_mode = True
