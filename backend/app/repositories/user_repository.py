from app.models import SolverUser
from app.repositories.base_repository import BaseRepository

class SolverUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(SolverUser)
