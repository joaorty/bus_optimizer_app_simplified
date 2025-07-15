from app.repositories import RepositoryManager
from app.models import Scenario
from sqlalchemy.orm import Session

class ScenarioService:
    def __init__(self):
        self.repository = RepositoryManager.get_scenario_repository()

    def create(self, user_id: int, name: str, description: str = None):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if not name or not isinstance(name, str):
            raise ValueError("name must be provided and must be a string.")

        scenario = Scenario(user_id=user_id, name=name, description=description)
        self.repository.save(scenario)
        return scenario.to_dict()

    def get_by_id(self, user_id: int, scenario_id: int):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if scenario_id is None or not isinstance(scenario_id, int):
            raise ValueError("scenario_id must be provided and must be an integer.")

        scenario = self.repository.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")
        return scenario.to_dict()

    def get_all(self, user_id: int, db_session: Session):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if db_session is None:
            raise ValueError("db_session must be provided.")

        scenarios = self.repository.find_all_by(user_id=user_id)
        if not scenarios:
            raise ValueError("No scenarios found for this user.")
        return [scenario.to_dict() for scenario in scenarios]

    def update(self, user_id: int, scenario_id: int, name: str = None, description: str = None):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if scenario_id is None or not isinstance(scenario_id, int):
            raise ValueError("scenario_id must be provided and must be an integer.")
        if name is not None and not isinstance(name, str):
            raise ValueError("name must be a string if provided.")
        if description is not None and not isinstance(description, str):
            raise ValueError("description must be a string if provided.")

        scenario = self.repository.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")

        if name:
            scenario.name = name
        if description:
            scenario.description = description
        self.repository.save(scenario)
        return scenario.to_dict()

    def delete(self, user_id: int, scenario_id: int):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if scenario_id is None or not isinstance(scenario_id, int):
            raise ValueError("scenario_id must be provided and must be an integer.")

        scenario = self.repository.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")
        self.repository.delete_with_session(scenario)
        return {"message": "Scenario deleted successfully."}
