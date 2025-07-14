from app.models import Route
from app.repositories.base_repository import BaseRepository

class RouteRepository(BaseRepository):
    def __init__(self):
        super().__init__(Route)
