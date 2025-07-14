from app.repositories import RepositoryManager
from app.models import Scenario
from sqlalchemy.orm import Session

class ScenarioService:
    def __init__(self):
        self.repository = RepositoryManager.get_scenario_repository()

    def create(self, name: str, description: str = None):
        scenario = Scenario(name=name, description=description)
        self.repository.save(scenario)
        return scenario.to_dict()

    def get_by_id(self, scenario_id: int):
        scenario = self.repository.find_first_by_id(scenario_id)
        if not scenario:
            raise ValueError("Scenario not found.")

        scenario_data = scenario.to_dict()

        return scenario_data

    def get_all(self, db_session: Session):
        scenarios = self.repository.find_all(db_session)
        if not scenarios:
            raise ValueError("No scenarios found.")
        return [ scenario.to_dict() for scenario in scenarios ]

    def update(self, scenario_id: int, name: str = None, description: str = None):
        scenario = self.repository.find_first_by_id(scenario_id)
        if not scenario:
            raise ValueError("Scenario not found.")

        if name:
            scenario.name = name
        if description:
            scenario.description = description

        self.repository.save(scenario)
        return scenario.to_dict()

    def delete(self, scenario_id: int):
        scenario = self.repository.find_first_by_id(scenario_id)
        if not scenario:
            raise ValueError("Scenario not found.")
        self.repository.delete_with_session(scenario)
        return {"message": "Scenario deleted successfully."}
