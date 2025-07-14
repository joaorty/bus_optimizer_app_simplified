from app.models import BusType
from app.repositories.base_repository import BaseRepository

class BusTypeRepository(BaseRepository):
    def __init__(self):
        super().__init__(BusType)
