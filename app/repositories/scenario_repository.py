from app.models import Scenario
from app.repositories.base_repository import BaseRepository

class ScenarioRepository(BaseRepository):
    def __init__(self):
        super().__init__(Scenario)
