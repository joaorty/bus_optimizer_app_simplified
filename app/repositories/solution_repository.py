from app.models import Solution
from app.repositories.base_repository import BaseRepository

class SolutionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Solution)
