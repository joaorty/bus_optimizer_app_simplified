from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScenarioBase(BaseModel):
  name: str
  description: Optional[str] = None

class ScenarioCreate(ScenarioBase):
  routes: List[RouteCreate]
  bus_types: List[BusTypeCreate]
  parameters: ParametersCreate

class ScenarioRead(ScenarioBase):
  id: int
  created_at: datetime
  updated_at: datetime

  routes: List[RouteRead]
  bus_types: List[BusTypeRead]
  parameters: ParametersRead

  class Config:
    orm_mode = True