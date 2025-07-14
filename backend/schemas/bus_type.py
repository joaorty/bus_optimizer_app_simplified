from pydantic import BaseModel
from typing import Optional

class BusTypeBase(BaseModel):
  scenario_id: int
  seat_capacity: int
  operational_cost_km: float
  load_factor: float
  available_units: int

class BusTypeCreate(BaseModel):
  seat_capacity: int
  operational_cost_km: float
  load_factor: float
  available_units: int

class BusTypeRead(BusTypeBase):
  id: int

  class Config:
    orm_mode = True