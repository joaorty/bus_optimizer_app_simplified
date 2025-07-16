from app.repositories import RepositoryManager
from app.models import Scenario, Route, BusType, Parameters
from sqlalchemy.orm import Session

class ScenarioService:
    def __init__(self):
        self.scenario_repository = RepositoryManager.get_scenario_repository()
        self.route_repository = RepositoryManager.get_route_repository()
        self.bus_type_repository = RepositoryManager.get_bus_type_repository()
        self.parameters_repository = RepositoryManager.get_parameters_repository()

    def create(
        self, user_id: int, name: str, description: str = None,
        list_routes = None, bus_types = None, parameters = None
    ):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if not name or not isinstance(name, str):
            raise ValueError("name must be provided and must be a string.")
        
        scenario = Scenario(user_id=user_id, name=name, description=description)
        scenario = self.scenario_repository.save(scenario)

        if list_routes is not None:
            for route in list_routes:
                route[ "scenario_id" ] = scenario.id
                if not self.route_repository.find_first_by( **route ):
                    new_route = Route( **route )
                    self.route_repository.save( new_route )
        
        if bus_types is not None:
            for bus_type in bus_types:
                bus_type[ "scenario_id" ] = scenario.id
                if not self.bus_type_repository.find_first_by( **bus_type ):
                    new_bus_type = BusType( **bus_type )
                    self.bus_type_repository.save( new_bus_type )
        
        if parameters is not None:
            parameters[ "scenario_id" ] = scenario.id
            if not self.parameters_repository.find_first_by( **parameters ):
                new_parameters = Parameters( **parameters )
                self.parameters_repository.save( new_parameters )

        return scenario.to_dict()

    def get_by_id(self, user_id: int, scenario_id: int):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if scenario_id is None or not isinstance(scenario_id, int):
            raise ValueError("scenario_id must be provided and must be an integer.")

        scenario = self.scenario_repository.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")
        return scenario.to_dict()

    def get_all(self, user_id: int, db_session: Session):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if db_session is None:
            raise ValueError("db_session must be provided.")

        scenarios = self.scenario_repository.find_all_by(user_id, db_session)
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

        scenario = self.scenario_repository.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")

        if name:
            scenario.name = name
        if description:
            scenario.description = description
        self.scenario_repository.save(scenario)
        return scenario.to_dict()

    def delete(self, user_id: int, scenario_id: int):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if scenario_id is None or not isinstance(scenario_id, int):
            raise ValueError("scenario_id must be provided and must be an integer.")

        scenario = self.scenario_repository.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")
        self.scenario_repository.delete_with_session(scenario)
        return {"message": "Scenario deleted successfully."}
