from app.models import Parameters
from app.repositories.base_repository import BaseRepository

class ParametersRepository(BaseRepository):
    def __init__(self):
        super().__init__(Parameters)
